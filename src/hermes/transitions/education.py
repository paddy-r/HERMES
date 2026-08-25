import numpy as np

from hermes.transitions.base import (
    TransitionModel
)


class Education(TransitionModel):

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

        education = (
            population.data.loc[
                alive,
                "education"
            ]
        )

        eligible = (
                education != "na"
        )

        education = education.loc[
            eligible
        ].astype(int)

        progress_eligible = (
                education < 9
        )

        u = np.random.random(
            size=progress_eligible.sum()
        )

        progress = (
                u < 0.05
        )

        print(
            f"Education progression: "
            f"{progress.sum()}"
        )

        indices = education.index[
            progress_eligible
        ][progress]

        population.data.loc[
            indices,
            "education"
        ] = (
                education.loc[
                    indices
                ] + 1
        )


class EducationLogit(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    intercept = -5.0

    coefficients = {
        "age": 0.05,
        "income": 0.00005,
        "education": -0.4,
    }

    def apply_transition(
        self,
        population
    ):

        alive = (
            population.data["life_status"]
            == "alive"
        )

        education = (
            population.data.loc[
                alive,
                "education"
            ]
        )

        eligible = (
            education != "na"
        )

        education = (
            education.loc[
                eligible
            ]
            .astype(int)
        )

        progress_eligible = (
            education < 9
        )

        indices = (
            education.index[
                progress_eligible
            ]
        )

        if len(indices) == 0:
            return

        logit = np.full(
            len(indices),
            self.intercept,
            dtype=float
        )

        for (
            predictor,
            coefficient
        ) in self.coefficients.items():

            values = (
                population.data.loc[
                    indices,
                    predictor
                ]
                .astype(float)
                .to_numpy()
            )

            logit += (
                coefficient
                * values
            )

        probability = (
            1.0
            /
            (
                1.0
                + np.exp(-logit)
            )
        )

        u = np.random.random(
            size=len(indices)
        )

        progress = (
            u < probability
        )

        print(
            f"Mean progression probability: "
            f"{probability.mean():.4f}"
        )

        print(
            f"Education progression: "
            f"{progress.sum()}"
        )

        progressed_indices = (
            indices[progress]
        )

        population.data.loc[
            progressed_indices,
            "education"
        ] = (
            education.loc[
                progressed_indices
            ]
            + 1
        )

