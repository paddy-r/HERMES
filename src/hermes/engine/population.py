# HR 29/07/26 Population classes, moved from earlier common script to its own

import pandas as pd


class Population:
    """Simple container for populations; variables are referred to as domains."""

    def __init__(
            self,
            data: pd.DataFrame,
            structure=None,
    ):

        self.data = data

        self.structure = (
            structure or {}
        )

        if self.structure:

            self.ensure_uids(
                verbose=True
            )

    def __repr__(self):

        return (
            f"<Population {self.data}>"
        )

    def ensure_uids(
            self,
            verbose=False
    ):

        structure = self.structure

        area_column = structure.get(
            "area_column"
        )

        # TODO:
        # Generalise UID generation to
        # N repeated levels.

        levels = structure.get(
            "levels",
            []
        )

        mixing = structure.get(
            "mixing",
            []
        )

        expected = max(
            len(levels) - 1,
            0
        )

        if len(mixing) == 0:

            mixing = [False] * expected

        if len(mixing) != expected:

            raise ValueError(
                f"Expected {expected} mixing values "
                f"for {len(levels)} levels, "
                f"received {len(mixing)}."
            )

        if any(mixing):

            raise NotImplementedError(
                "Mixed clone reconstruction "
                "not yet implemented."
            )

        if verbose:

            print(
                "\nPopulation structure\n"
                f"  Area column      : {area_column}\n"
                f"  Levels           : {levels}\n"
                f"  Mixing strategy  : {mixing}\n"
                f"  Population size  : {len(self.data)}"
            )

            for i, level in enumerate(levels):

                print(
                    f"  level_{i}_uid"
                    f" -> {level}"
                )

            print(
                "\nResolving clones..."
            )

        if area_column is None:

            areas = [
                ("ALL", self.data)
            ]

        else:

            areas = list(
                self.data.groupby(
                    area_column,
                    sort=False
                )
            )

        if not levels:

            if verbose:

                print(
                    "No repeated levels specified."
                )

            return

        household_column = levels[0]

        individual_column = levels[-1]

        #
        # Diagnostics only
        #

        for area_name, area_data in areas:

            households = (
                area_data[
                    household_column
                ]
                .unique()
            )

            if verbose:

                print(
                    f"\n=== Area: "
                    f"{area_name} ==="
                )

                print(
                    f"Households: "
                    f"{len(households)}"
                )

            for household in households:

                hh_data = area_data.loc[
                    area_data[
                        household_column
                    ] == household
                ]

                residents = sorted(
                    hh_data[
                        individual_column
                    ]
                    .unique()
                )

                clone_count = (
                    hh_data[
                        individual_column
                    ]
                    .value_counts()
                    .max()
                )

                if verbose:

                    print(
                        f"{household} "
                        f"(clones={clone_count})"
                    )

                    print(
                        f"Residents: "
                        f"{residents}"
                    )

        #
        # Assign UIDs
        #

        if verbose:

            print(
                "\nAssigning UIDs..."
            )

        # Lowest repeated level:
        # every row becomes a unique entity.

        self.data[
            "level_1_uid"
        ] = range(
            len(self.data)
        )

        # Highest repeated level:
        # reconstruct household instances.

        self.data[
            "level_0_uid"
        ] = -1

        level_0_uid_counter = 0

        for area_name, area_data in areas:

            for household in (
                    area_data[
                        household_column
                    ]
                    .unique()
            ):

                hh_data = area_data.loc[
                    area_data[
                        household_column
                    ] == household
                ]

                clone_count = (
                    hh_data[
                        individual_column
                    ]
                    .value_counts()
                    .max()
                )

                household_uids = [
                    level_0_uid_counter + i
                    for i in range(
                        clone_count
                    )
                ]

                level_0_uid_counter += (
                    clone_count
                )

                residents = sorted(
                    hh_data[
                        individual_column
                    ]
                    .unique()
                )

                for resident in residents:

                    resident_rows = hh_data.loc[
                        hh_data[
                            individual_column
                        ] == resident
                    ]

                    for i, idx in enumerate(
                            resident_rows.index
                    ):

                        self.data.loc[
                            idx,
                            "level_0_uid"
                        ] = household_uids[i]

        if verbose:

            print(
                f"Created "
                f"{level_0_uid_counter} "
                f"level_0 UIDs"
            )

            print(
                f"Created "
                f"{len(self.data)} "
                f"level_1 UIDs"
            )

            print(
                self.data[
                    [
                        area_column,
                        household_column,
                        individual_column,
                        "level_0_uid",
                        "level_1_uid"
                    ]
                ]
                .head(50)
            )
