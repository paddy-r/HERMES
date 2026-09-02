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


class TimeRegression(TransitionModel):

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

        predictor_names = (
            self.rate_source.predictors
        )

        response_domain = (
            self.rate_source.response
        )

        income_before = (
            population.data.loc[
                alive,
                response_domain
            ]
            .astype(float)
            .copy()
        )

        predictor_data = (
            population.data.loc[
                alive,
                predictor_names
            ]
        )

        predicted_values = (
            self.rate_source.predict(
                predictor_data.to_numpy()
            )
        )

        population.data[
            response_domain
        ] = (
            population.data[
                response_domain
            ].astype(float)
        )

        population.data.loc[
            alive,
            response_domain
        ] = predicted_values

        population.data.loc[
            alive,
            response_domain
        ] = predicted_values

        mean_income_before = (
            income_before.mean()
        )

        mean_income_after = (
            predicted_values.mean()
        )

        print(
            f"Mean income before: "
            f"{mean_income_before:.2f}"
        )

        print(
            f"Mean income after: "
            f"{mean_income_after:.2f}"
        )

        growth_factor = (
                mean_income_after
                /
                mean_income_before
        )

        print(
            f"Mean growth factor: "
            f"{growth_factor:.6f}"
        )
