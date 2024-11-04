from supermarkt_base.supermarkt_base_class import GiftCardVerifier

class ReweVerifier(GiftCardVerifier):
    def verify_gift_card(self, card_number, pin):
        print(f"Verifiziere Gutschein von Rewe: Nummer = {card_number}, Pin = {pin}")

