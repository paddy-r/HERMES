from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class RateTableVerifier(Verifier):

    priority = 40

    def _verify(self, simulation):
        pass
