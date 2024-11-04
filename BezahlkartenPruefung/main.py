from supermarkt_navigation import EdekaVerifier, DmVerifier

#Edeka
#0200240013627693912

#DM
#Code: 905100192700380827566272
#Pin: 6789

if __name__ == "__main__":
    def main():
        supermarkt_name = input("Bitte geben Sie den Supermarktname ein: ")
        print("Kartennummer und PIN eingeben...")
        card_number = input("Bitte geben Sie die Gutscheinnummer ein: ")
        pin = input("Bitte geben Sie die PIN ein: ")
        # Erstellen einer Instanz von EdekaVerifier und testen
        if supermarkt_name == "Edeka":
            edeka_verifier = EdekaVerifier()
            edeka_verifier.open_website()
            edeka_verifier.verify_gift_card(card_number, pin)
        elif supermarkt_name == "Dm":
            dm_verifier = DmVerifier()
            dm_verifier.open_website()
            dm_verifier.verify_gift_card(card_number, pin)

    # Beispielaufruf
    main()