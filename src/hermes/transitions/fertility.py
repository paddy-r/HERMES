import numpy as np
import pandas as pd
from hermes.transitions.base import TransitionModel


class Fertility(TransitionModel):

    creates_domains = {"life_status": "alive"}

    def create_newborns(self, population, mothers):
        newborns = mothers.copy()

        print(
            f"Creating "
            f"{len(newborns)} newborns"
        )

        newborns["demographic_id"] = "na"
        newborns["age"] = 0
        newborns["education"] = "na"
        newborns["family_ratio"] = 0
        newborns["income"] = 0
        newborns["relationship"] = "child"
        newborns["life_status"] = "alive"
        newborns["gender"] = np.random.randint(0, 2, size=len(newborns))

        max_id = population.data["id"].max()
        newborns["id"] = [
            f"newborn_{i}"
            for i in range(
                len(population.data),
                len(population.data) + len(newborns)
            )
        ]

        population.data = pd.concat(
            [
                population.data,
                newborns
            ],
            ignore_index=True
        )

    def apply_transition(self, population):

        alive = (
            population.data["life_status"]
            == "alive"
        )

        eligible = (
            alive
            &
            (population.data["gender"] == 1)
        )

        domains = {
            domain: population.data.loc[
                eligible,
                domain
            ]
            for domain in self.rate_source.domains
        }

        rates = self.rate_source.evaluate(
            domains
        )

        u = np.random.random(
            len(rates)
        )

        births = u < rates

        print(
            f"Births this step: "
            f"{births.sum()}"
        )

        mothers = population.data.loc[eligible].loc[births]
        self.create_newborns(population, mothers)


class FertilityParity(Fertility):

    creates_domains = {
        "life_status": "alive",
        "parity": 0
    }
