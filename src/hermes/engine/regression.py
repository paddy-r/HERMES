import json
import pickle
import os
import pandas as pd
from hermes import utilities as hutils
from hermes.regressions.base import RegressionModel
from hermes.constants import WAVE_DATA_PREFIX, WAVE_DATA_SUFFIX

REGRESSION_ALIASES = {
    "linear": "LinearRegressionModel",
    "logistic": "LogisticRegressionModel",
    "fixed": "FixedEffectsModel",
    "random": "RandomEffectsModel",
    "survival": "SurvivalModel",
    "eventhistory": "EventHistoryModel",
}


class Regression:

    def __init__(
        self,
        spec
    ):
        self.spec = spec

        print(
            "Initialising Regression model handler"
        )

        if spec.get("group", False):
            raise NotImplementedError(
                "Grouped regression training "
                "not yet implemented."
            )

    def get_regression_class(self):

        regression_name = (
            REGRESSION_ALIASES.get(
                self.spec["regression"],
                self.spec["regression"]
            )
        )

        return (
            regression_name,
            RegressionModel.registry[
                regression_name
            ]
        )

    def verify(self):

        print(
            "Verifying Regression model handler"
        )

        if not self.spec["predictors"]:
            raise ValueError(
                "At least one predictor "
                "must be supplied."
            )

        if not self.spec["response"]:
            raise ValueError(
                "A response variable "
                "must be supplied."
            )

        regression_name, regression_class = (
            self.get_regression_class()
        )

        data_path, wave_files = (
            self.get_training_data()
        )

        uid_column = (
            self.get_uid_column()
        )

        if uid_column is not None:

            wave = pd.read_csv(
                os.path.join(
                    data_path,
                    wave_files[0]
                )
            )

            if uid_column not in wave.columns:
                raise ValueError(
                    f"UID column "
                    f"'{uid_column}' "
                    f"not found in "
                    f"{wave_files[0]}."
                )

        minimum_waves = getattr(
            regression_class,
            "minimum_waves",
            1
        )

        if len(wave_files) < minimum_waves:
            raise ValueError(
                f"{regression_class.__name__} "
                f"requires at least "
                f"{minimum_waves} waves "
                f"of training data. "
                f"Found only "
                f"{len(wave_files)}."
            )

    def get_training_data(self):

        def get_wave_number(
                filename,
                wave_prefix,
                wave_suffix
        ):

            return int(
                filename
                .replace(
                    wave_prefix,
                    ""
                )
                .replace(
                    wave_suffix,
                    ""
                )
            )

        if self.spec.get(
                "training_path"
        ) is not None:

            data_path = (
                self.spec["training_path"]
            )

        else:

            data_path = (
                hutils.get_latest_by_config(
                    universe=self.spec["universe"],
                    config=self.spec["config"]
                )
            )

        wave_prefix = self.spec.get(
            "wave_prefix",
            WAVE_DATA_PREFIX
        )

        wave_suffix = self.spec.get(
            "wave_suffix",
            WAVE_DATA_SUFFIX
        )

        wave_files = sorted(
            [
                file
                for file in os.listdir(
                data_path
            )
                if file.startswith(
                wave_prefix
            )
                   and file.endswith(
                wave_suffix
            )
            ],
            key=lambda x:
            get_wave_number(
                x,
                wave_prefix,
                wave_suffix
            )
        )

        print(
            f"Found "
            f"{len(wave_files)} "
            f"wave files\n"
        )

        return (
            data_path,
            wave_files
        )

    def get_uid_column(self):

        return self.spec.get(
            "uid"
        )

    def create_training_dataset(
            self,
            data_path,
            wave_files
    ):

        uid_column = (
            self.get_uid_column()
        )

        datasets = []

        print(
            "\nCreating training dataset..."
        )

        for i in range(
                len(wave_files) - 1
        ):
            current_file = wave_files[i]

            next_file = wave_files[i + 1]

            print(
                f"{current_file} "
                f"-> "
                f"{next_file}"
            )

            current_wave = pd.read_csv(
                os.path.join(
                    data_path,
                    current_file
                )
            )

            next_wave = pd.read_csv(
                os.path.join(
                    data_path,
                    next_file
                )
            )

            if uid_column is None:

                #
                # No UIDs
                #

                pair_training_data = (
                    current_wave[
                        self.spec["predictors"]
                    ]
                    .copy()
                )

                pair_training_data[
                    self.spec["response"]
                ] = next_wave[
                    self.spec["predictors"][0]
                ]

            else:

                #
                # With UID matching
                #

                merged = current_wave.merge(
                    next_wave,
                    on=uid_column,
                    suffixes=(
                        "_current",
                        "_next"
                    )
                )

                pair_training_data = pd.DataFrame()

                for predictor in self.spec["predictors"]:
                    pair_training_data[predictor] = (
                        merged[
                            predictor + "_current"
                            ]
                    )

                pair_training_data[
                    self.spec["response"]
                ] = (
                    merged[
                        self.spec["predictors"][0]
                        + "_next"
                        ]
                )

            datasets.append(
                pair_training_data
            )

        training_data = pd.concat(
            datasets,
            ignore_index=True
        )

        print(
            "Training dataset shape:",
            training_data.shape
        )

        print(
            "Training rows:",
            len(training_data)
        )

        print(
            "Expected rows:",
            (
                    len(wave_files) - 1
            )
            * len(current_wave)
        )

        return training_data

    def save_model(
            self,
            regression,
            regression_class,
            fullpath,
            training_data
    ):

        with open(fullpath, "wb") as f:
            pickle.dump(
                regression,
                f
            )

        print(
            f"Created regression artefact:\n"
            f"{fullpath}"
        )

        metadata = {
            "regression_type":
                regression_class.__name__,

            "predictors":
                self.spec["predictors"],

            "response":
                self.spec["response"],

            "training_config":
                self.spec["config"],

            "training_universe":
                self.spec["universe"],

            "timestamp":
                hutils.get_timestamp(),

            "training_rows":
                len(training_data),
        }

        metadata.update(
            regression.get_metadata()
        )

        json_path = (
            fullpath.replace(
                ".pkl",
                ".json"
            )
        )

        with open(
            json_path,
            "w"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )

        print(
            f"Created regression metadata:\n"
            f"{json_path}"
        )

    def run(self):

        print(
            "Running Regression model handler"
        )

        print(
            "Available regression models:"
        )

        print(
            list(
                RegressionModel.registry.keys()
            )
        )

        regression_name, regression_class = (
            self.get_regression_class()
        )

        print(
            f"Selected regression model: "
            f"{regression_class.__name__}"
        )

        regression = regression_class()

        regression_path = (
            hutils.get_regression_path(
                self.spec["universe"]
            )
        )

        filename = (
                self.spec["config"]
                + "__"
                + regression_name
                + ".pkl"
        )

        fullpath = os.path.join(
            regression_path,
            filename
        )

        data_path, wave_files = (
            self.get_training_data()
        )

        training_data = (
            self.create_training_dataset(
                data_path,
                wave_files
            )
        )

        X = training_data[
            self.spec["predictors"]
        ].to_numpy()

        y = training_data[
            self.spec["response"]
        ].to_numpy()

        regression.fit(
            X,
            y
        )

        self.save_model(
            regression=regression,
            regression_class=regression_class,
            fullpath=fullpath,
            training_data=training_data
        )
