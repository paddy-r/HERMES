import numpy as np
from hermes.transitions.base import TransitionModel


class ComingOfAge(TransitionModel):

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

        eligible = (
            alive
            &
            (population.data["age"] == 16)
        )

        print(
            f"Coming of age: "
            f"{eligible.sum()}"
        )

        if eligible.sum() == 0:
            return

        adult_categories = [
            category
            for category in population.data[
                "demographic_id"
            ].dropna().unique()
            if category != "na"
        ]

        population.data.loc[
            eligible,
            "demographic_id"
        ] = np.random.choice(
            adult_categories,
            size=eligible.sum()
        )

        population.data.loc[
            eligible,
            "income"
        ] = np.random.normal(
            loc=5000,
            scale=1000,
            size=eligible.sum()
        )

        population.data.loc[
            eligible,
            "relationship"
        ] = "child"

        population.data.loc[
            eligible,
            "education"
        ] = np.random.choice(
            [2, 1, 0],
            size=eligible.sum(),
            p=[4 / 7, 2 / 7, 1 / 7]
        )
