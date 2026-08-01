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
        ).astype(str)
