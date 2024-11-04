from flask import Flask, request, render_template, send_file
from supermarkt_navigation import DmVerifier, EdekaVerifier
import os

app = Flask(__name__)

# Erstellen Sie Instanzen der Verifier
verifiers = {
    "dm": DmVerifier(),
    "edeka": EdekaVerifier()
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    captcha_image = None

    if request.method == "POST":
        supermarket = request.form.get("supermarket")
        card_number = request.form.get("card_number")
        pin = request.form.get("pin")
        captcha_code = request.form.get("captcha_code")

        verifier = verifiers.get(supermarket)
        if not verifier:
            error = "Ungültiger Supermarkt."
        else:
            try:
                # Öffne die Website
                verifier.open_website()
                # Gebe Kartennummer und PIN ein
                if supermarket == "edeka":
                    verifier.solve_captcha_in_background('/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[1]/div[1]')
                    part1 = card_number[:5]
                    part2 = card_number[5:]
                    verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[1]', part1,"Erster Teil der Kartennummer")
                    verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[2]', part2,"Zweiter Teil der Kartennummer")
                    verifier.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[1]/div/div/input', pin,"PIN")

                else:
                    verifier.enter_input("/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[1]/input",card_number, "Kartennummer")
                    verifier.enter_input("/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[3]/input",pin, "PIN")
                # Captcha im Hintergrund lösen
                captcha_path = "captcha_image.png"
                if os.path.exists(captcha_path):
                    captcha_image = captcha_path
                # Wenn Captcha vorhanden, mit dem Code abschließen
                if captcha_code:
                    if supermarket == "edeka":
                        verifier.solve_captcha(
                            '/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[2]/input[1]')
                    # Formular absenden und Gutscheinwert abrufen
                    balance = verifier.get_balance(
                        "/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/div[2]/div/div[4]/div/p/strong")
                    result = f"Gutscheinwert: {balance}"
            except Exception as e:
                error = str(e)

    return render_template("index.html", result=result, error=error, captcha_image=captcha_image)

@app.route("/captcha-image")
def captcha_image():
    captcha_path = "captcha_image.png"
    if os.path.exists(captcha_path):
        return send_file(captcha_path, mimetype='image/png')
    else:
        return "Captcha-Bild nicht gefunden", 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)