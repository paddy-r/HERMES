import numpy as np
import pandas as pd
from hermes.transitions.base import TransitionModel


class MigrationInternal(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(
        self,
        population
    ):

        households = (
            population.data[
                "household_id"
            ]
            .unique()
        )

        move = (
            np.random.random(
                size=len(households)
            ) < 0.01
        )

        migrating_households = (
            households[move]
        )

        print(
            f"Internal migrations: "
            f"{len(migrating_households)} households"
        )

        areas = (
            population.data[
                "area_id"
            ]
            .unique()
        )

        for household_id in (
            migrating_households
        ):

            current_area = (
                population.data.loc[
                    population.data[
                        "household_id"
                    ] == household_id,
                    "area_id"
                ]
                .iloc[0]
            )

            possible_areas = (
                areas[
                    areas != current_area
                ]
            )

            destination = np.random.choice(
                possible_areas
            )

            population.data.loc[
                population.data[
                    "household_id"
                ] == household_id,
                "area_id"
            ] = destination


class MigrationOut(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(
        self,
        population
    ):

        households = (
            population.data[
                "household_id"
            ]
            .unique()
        )

        out = np.random.random(
            size=len(households)
        ) < 0.01

        households_out = households[out]

        print(
            f"Outward migrations: "
            f"{len(households_out)} households"
        )

        population.data = population.data.loc[
            ~population.data[
                "household_id"
            ].isin(
                households_out
            )
        ].reset_index(
            drop=True
        )


class MigrationIn(TransitionModel):

    creates_domains = {
        "life_status": "alive"
    }

    def apply_transition(
        self,
        population
    ):

        households = (
            population.data[
                "household_id"
            ]
            .unique()
        )

        incoming = (
            np.random.random(
                size=len(households)
            ) < 0.01
        )

        households_in = households[
            incoming
        ]

        print(
            f"Inward migrations: "
            f"{len(households_in)} households"
        )

        if len(households_in) == 0:
            return

        migrants = []

        areas = (
            population.data[
                "area_id"
            ]
            .unique()
        )

        population_size = len(
            population.data
        )

        for i, household_id in enumerate(
            households_in
        ):

            household = (
                population.data.loc[
                    population.data[
                        "household_id"
                    ] == household_id
                ].copy()
            )

            current_area = (
                household[
                    "area_id"
                ].iloc[0]
            )

            possible_areas = (
                areas[
                    areas != current_area
                ]
            )

            household[
                "area_id"
            ] = np.random.choice(
                possible_areas
            )

            household[
                "household_id"
            ] = (
                f"hh_migrant_"
                f"{population_size + i}"
            )

            migrants.append(
                household
            )

        migrants = pd.concat(
            migrants,
            ignore_index=True
        )

        migrants["id"] = [
            f"migrant_{i}"
            for i in range(
                len(population.data),
                len(population.data)
                + len(migrants)
            )
        ]

        population.data = pd.concat(
            [
                population.data,
                migrants
            ],
            ignore_index=True
        )
