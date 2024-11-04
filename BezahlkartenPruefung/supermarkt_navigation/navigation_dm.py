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
from supermarkt_base.supermarkt_base_class import GiftCardVerifier

class DmVerifier(GiftCardVerifier):
    def verify_gift_card(self, card_number, pin):
        try:
            #print("\u00d6ffne die Website...")
            #self.open_website()
            #print("Kartennummer und PIN eingeben...")
            #card_number = input("Bitte geben Sie die Gutscheinnummer ein: ")
            #pin = input("Bitte geben Sie die PIN ein: ")

            self.enter_input('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[1]/input', card_number, "Kartennummer")
            self.enter_input('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/div[3]/input', pin, "PIN")

            print("Formular absenden...")
            self.submit_form('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/form/button', '/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/div[2]/div/div[4]/div/p/strong')
            print("Gutscheinwert abrufen...")
            balance = self.get_balance('/html/body/div[1]/div/main/div[2]/div/div[8]/div/div/div/div[2]/div/div[4]/div/p/strong')
            balance_value = self.extract_balance_value(balance)
            print(f"Gutscheinwert: {balance_value}")
        except:
            print("Der Gutschein ist ungültig")
        finally:
            self.driver.quit()

    def open_website(self):
        # Öffne die DM Gutscheinseite
        self.driver.get('https://www.dm.de/services/services-im-markt/geschenkkarten#abfrage-guthaben')