from supermarkt_navigation import ReweVerifier, DmVerifier, EdekaVerifier


class VerifierFactory:
    _verifiers = {
        'dm': DmVerifier,
        'rewe': ReweVerifier,
        'edeka': EdekaVerifier
    }

    @staticmethod
    def get_verifier(supermarket_name):
        verifier_class = VerifierFactory._verifiers.get(supermarket_name.lower())
        if not verifier_class:
            raise ValueError(f"Verifier für {supermarket_name} nicht gefunden.")
        return verifier_class()

    @staticmethod
    def get_verifiers():
        return [verifier for verifier in VerifierFactory._verifiers.keys()]
