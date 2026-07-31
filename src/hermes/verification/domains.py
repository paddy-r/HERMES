from hermes.verification.base import Verifier
from hermes.errors import VerificationError


class DomainVerifier(Verifier):

    priority = 50

    def _verify(self, simulation):

        for model in simulation.models:

            for domain, default in (
                model.creates_domains.items()
            ):

                if domain not in (
                    simulation.population.data.columns
                ):

                    print(
                        f"Creating domain "
                        f"'{domain}' "
                        f"with default value "
                        f"'{default}'"
                    )

                    simulation.population.data[
                        domain
                    ] = default
