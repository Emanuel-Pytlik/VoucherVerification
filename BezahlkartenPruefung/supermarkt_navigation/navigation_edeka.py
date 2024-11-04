from supermarkt_base.supermarkt_base_class import GiftCardVerifier

class EdekaVerifier(GiftCardVerifier):
    def verify_gift_card(self, card_number, pin):
        try:
            print("\u00d6ffne die Website...")
            #self.open_website()
            print("Captcha im Hintergrund lösen...")
            self.solve_captcha_in_background('/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[1]/div[1]')
            part1 = str(card_number)[:5]
            part2 = str(card_number)[5:]
            #self.enter_card_and_pin(pin, part1, part2)
            self.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[1]', part1, "Erster Teil der Kartennummer")
            self.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[2]/div/input[2]', part2, "Zweiter Teil der Kartennummer")
            self.enter_input('/html/body/app-root/app-verification-page/main/div/div[2]/div[3]/div[1]/div/div/input', pin, "PIN")
            print("Captcha eingeben...")
            self.solve_captcha('/html/body/app-root/app-verification-page/main/div/div[2]/app-captcha/div/div[2]/input[1]')
            print("Formular absenden...")
            self.submit_form('/html/body/app-root/app-verification-page/main/div/div[2]/button','/html/body/app-root/app-balance-page/main/div/div[2]/div/div/div[1]/div[1]/p/span[2]' )
            print("Gutscheinwert abrufen...")
            balance = self.get_balance('/html/body/app-root/app-balance-page/main/div/div[2]/div/div/div[1]/div[1]/p/span[2]')
            print(f"Gutscheinwert: {balance}")
        finally:
            self.driver.quit()

    def open_website(self):
        # Öffne die Edeka Gutscheinseite
        self.driver.get('https://evci.pin-host.com/evci/#/guthabenabfrage')
