from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class PopulationVerifier(Verifier):

    priority = 10

    def _verify(self, simulation):

        if simulation.population is None:

            raise VerificationError(
                "Input population could not be loaded."
            )

        if simulation.population.data.empty:

            raise VerificationError(
                "Input population is empty."
            )
