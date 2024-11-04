from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel
from supermarkt_navigation import DmVerifier, EdekaVerifier
from enum import Enum
from starlette.middleware.base import BaseHTTPMiddleware
import os

app = FastAPI()

# Enum for supermarket selection
class Supermarket(str, Enum):
    dm = "dm"
    edeka = "edeka"

# Response model for Captcha
class CaptchaResponse(BaseModel):
    captcha_image_path: str

# Response model for GiftCard balance
class BalanceResponse(BaseModel):
    balance: str

# Stores instances of verifiers
gift_card_verifiers = {
    "dm": DmVerifier(),
    "edeka": EdekaVerifier()
}

# Middleware to initialize verifiers on first request
class StartupMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, verifiers):
        super().__init__(app)
        self.verifiers = verifiers
        self.initialized = False

    async def dispatch(self, request: Request, call_next):
        if not self.initialized:
            # Webseiten im Voraus laden
            for verifier in self.verifiers.values():
                verifier.open_website()
            self.initialized = True
            print("Initialisierung abgeschlossen, Webseiten geladen.")

        response = await call_next(request)
        return response

# Füge die Middleware hinzu
app.add_middleware(StartupMiddleware, verifiers=gift_card_verifiers)



# Endpoint to start the gift card verification (for supermarkets with captcha)
@app.post("/start-verification-with-captcha/", response_model=CaptchaResponse)
async def start_verification_with_captcha(supermarket: Supermarket, card_number: str = Form(...), pin: str = Form(...)):
    verifier = gift_card_verifiers.get(supermarket.value)
    if not verifier:
        raise HTTPException(status_code=404, detail="Supermarket not supported")
    try:
        print(f"Öffne die Website für {supermarket}...")
        #verifier.open_website()

        if supermarket == Supermarket.dm:
            verifier.enter_input('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[1]/input', card_number, "Kartennummer")
            verifier.enter_input('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[3]/input', pin, "PIN")
            verifier.solve_captcha_in_background('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[5]/div/div/img')
        elif supermarket == Supermarket.edeka:
            # Split card number for Edeka verifier
            part1 = card_number[:5]
            part2 = card_number[5:]
            verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[1]', part1, "Erster Teil der Kartennummer")
            verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[2]', part2, "Zweiter Teil der Kartennummer")
            verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[1]/div/div/input', pin, "PIN")
            verifier.solve_captcha_in_background('/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[1]/div[1]')

        captcha_image_path = "captcha_image.png"
        if not os.path.exists(captcha_image_path):
            raise HTTPException(status_code=500, detail="Captcha image could not be generated")

        return CaptchaResponse(captcha_image_path=captcha_image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        verifier.driver.quit()

# Endpoint to complete the verification by providing the captcha code
@app.post("/complete-verification-with-captcha/", response_model=BalanceResponse)
async def complete_verification_with_captcha(supermarket: Supermarket, captcha_code: str = Form(...)):
    verifier = gift_card_verifiers.get(supermarket.value)
    if not verifier:
        raise HTTPException(status_code=404, detail="Supermarket not supported")
    try:
        print(f"Löse das Captcha für {supermarket}...")
        if supermarket == Supermarket.dm:
            verifier.solve_captcha('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[5]/div/div/input')
        elif supermarket == Supermarket.edeka:
            verifier.solve_captcha('/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[2]/input[1]')

        print("Formular absenden...")
        if supermarket == Supermarket.dm:
            verifier.submit_form('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/button')
        elif supermarket == Supermarket.edeka:
            verifier.submit_form('/html/body/app-root/app-verification-page/main/div/div[2]/button')

        print("Gutscheinwert abrufen...")
        if supermarket == Supermarket.dm:
            balance = verifier.get_balance('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/div[2]/div/div[4]/div/p/strong')
            balance_value = verifier.extract_balance_value(balance)
        elif supermarket == Supermarket.edeka:
            balance = verifier.get_balance('/html/body/app-root/app-balance-page/main/div/div[2]/div/div/div[1]/div[1]/p/span[2]')
            balance_value = verifier.extract_balance_value(balance)

        return BalanceResponse(balance=balance_value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        verifier.driver.quit()

# Endpoint for supermarkets without captcha
@app.post("/verify-gift-card/", response_model=BalanceResponse)
async def verify_gift_card(supermarket: Supermarket, card_number: str = Form(...), pin: str = Form(...)):
    verifier = gift_card_verifiers.get(supermarket.value)
    if not verifier:
        raise HTTPException(status_code=404, detail="Supermarket not supported")
    try:
        print(f"Öffne die Website für {supermarket}...")
        verifier.open_website()
        return verifier.verify_gift_card(card_number, pin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        verifier.driver.quit()