import numpy as np
from hermes.transitions.base import TransitionModel


class Time(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(self, population):

        alive = (
            population.data["life_status"]
            == "alive"
        )

        population.data.loc[
            alive,
            "age"
        ] += 1

        population.data["income"] = (
            population.data["income"]
            .astype(float)
        )

        population.data.loc[
            alive,
            "income"
        ] *= 1.02

        print(
            f"Population size: "
            f"{len(population.data)}"
        )


class TimeStochastic(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(self, population):

        alive = (
            population.data["life_status"]
            == "alive"
        )

        population.data.loc[
            alive,
            "age"
        ] += 1

        growth = np.random.normal(
            loc=0.02,
            scale=0.01,
            size=alive.sum()
        )

        print(
            f"Mean growth: {growth.mean():.4f}"
        )

        print(
            f"Std growth : {growth.std():.4f}"
        )

        print(
            f"Min growth : {growth.min():.4f}"
        )

        print(
            f"Max growth : {growth.max():.4f}"
        )

        population.data["income"] = (
            population.data["income"]
            .astype(float)
        )

        population.data.loc[
            alive,
            "income"
        ] *= (1 + growth)
