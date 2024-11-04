from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import re


class GiftCardVerifier(ABC):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    @abstractmethod
    def verify_gift_card(self):
        pass

    @abstractmethod
    def open_website(self):
        pass

    def solve_captcha_in_background(self, captcha_xpath):
        wait = WebDriverWait(self.driver, 3)
        print("Warte auf das Captcha-Element...")
        captcha_element = wait.until(EC.presence_of_element_located((By.XPATH, captcha_xpath)))
        print(f"Captcha-Element gefunden: {captcha_element}")
        captcha_screenshot = captcha_element.screenshot_as_png

        # Speichern Sie den Screenshot in einer Datei
        with open("captcha_image.png", "wb") as file:
            file.write(captcha_screenshot)

        print("Captcha-Bild wurde gespeichert als 'captcha_image.png'.")

    def solve_captcha(self, captcha_input_xpath):
        captcha_code = input("Bitte geben Sie den Captcha-Code ein: ")
        wait = WebDriverWait(self.driver, 0.1)
        print("Warte auf das Captcha-Eingabefeld...")
        captcha_input = wait.until(EC.element_to_be_clickable((By.XPATH, captcha_input_xpath)))
        print(f"Captcha-Eingabefeld ist interaktiv: {captcha_input}")
        self.driver.execute_script("arguments[0].scrollIntoView();", captcha_input)
        captcha_input.send_keys(captcha_code)
        time.sleep(3)

    def enter_input(self, input_xpath, value, description="Eingabefeld"):
        wait = WebDriverWait(self.driver, 40)
        print(f"Warte auf das {description}...")
        input_element = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView();", input_element)
        input_element = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        print(f"{description} gefunden und interaktiv: {input_element}")
        try:
            input_element.click()
            input_element.send_keys(value)
        except ElementClickInterceptedException:
            print(f"Ein Überlagerungselement blockiert das {description}. Versuche, es zu entfernen...")
            self.driver.execute_script("arguments[0].style.display = 'none';", self.driver.find_element(By.ID, 'usercentrics-root'))
            input_element.click()
            input_element.send_keys(value)
        time.sleep(0.5)

    def submit_form(self, submit_button_xpath, expected_xpath_after_submit):
        wait = WebDriverWait(self.driver, 40)
        print("Warte auf den Absenden-Button...")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
        print(f"Absenden-Button gefunden und interaktiv: {submit_button}")
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)

        attempt = 0
        max_attempts = 3

        while attempt < max_attempts:
            submit_button.click()
            print(f"Versuche, den Absenden-Button zu klicken (Versuch {attempt + 1}/{max_attempts})...")

            try:
                # Überprüfe, ob das erwartete Element nach dem Absenden erscheint
                wait.until(EC.presence_of_element_located((By.XPATH, expected_xpath_after_submit)))
                print("Absenden-Button erfolgreich geklickt und Aktion ausgeführt.")
                return
            except TimeoutException:
                print("Aktion nach dem Absenden-Button-Klick nicht bestätigt. Erneuter Versuch.")
                attempt += 1

        print("Maximale Anzahl der Versuche erreicht. Aktion konnte nicht bestätigt werden.")
        raise TimeoutException("Aktion nach dem Absenden-Button-Klick nicht bestätigt.")

    def wait_for_page_change(self, balance_xpath):
        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, balance_xpath)))
        except TimeoutException:
            print("Timeout beim Laden der Seite. Stellen Sie sicher, dass die Seite korrekt geladen wurde.")
            self.driver.save_screenshot("page_load_error.png")
            print("Screenshot der aktuellen Seite wurde gespeichert als 'page_load_error.png'.")

    def get_balance(self, balance_xpath):
        try:
            wait = WebDriverWait(self.driver, 60)
            print("Warte auf das Balance-Element...")
            balance_element = wait.until(EC.presence_of_element_located((By.XPATH, balance_xpath)))
            print(f"Balance-Element gefunden: {balance_element}")
            return balance_element.text
        except TimeoutException:
            print("Timeout beim Laden der Seite. Stellen Sie sicher, dass die Seite korrekt geladen wurde.")
            self.driver.save_screenshot("page_load_error.png")
            print("Screenshot der aktuellen Seite wurde gespeichert als 'page_load_error.png'.")


    def extract_balance_value(self, balance_text):
        match = re.search(r'(\d{1,3}(\.\d{3})*,\d{2})', balance_text)
        if match:
            return match.group(1)
        return "Unbekannter Betrag"