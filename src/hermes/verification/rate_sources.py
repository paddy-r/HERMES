from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class RateSourceVerifier(Verifier):

    priority = 30

    def _verify(self, simulation):
        pass
