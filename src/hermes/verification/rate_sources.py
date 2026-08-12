from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class SourceVerifier(Verifier):

    priority = 30

    def _verify(self, simulation):
        pass
