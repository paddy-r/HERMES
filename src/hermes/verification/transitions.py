from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class TransitionVerifier(Verifier):

    priority = 20

    def _verify(self, simulation):

        if not simulation.spec["transitions"]:

            raise VerificationError(
                "No transitions specified."
            )
