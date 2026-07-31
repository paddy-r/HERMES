import numpy as np
from hermes.transitions.base import TransitionModel


class Mortality(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(
        self,
        population
    ):

        alive = (
            population.data["life_status"]
            == "alive"
        )

        domains = {
            domain: population.data.loc[
                alive,
                domain
            ]
            for domain in self.rate_source.domains
        }

        rates = self.rate_source.evaluate(
            domains
        )

        u = np.random.random(
            size=alive.sum()
        )

        deaths = u < rates

        print(
            f"Deaths this step: "
            f"{deaths.sum()}"
        )

        population.data.loc[
            population.data.index[alive][deaths],
            "life_status"
        ] = "dead"
