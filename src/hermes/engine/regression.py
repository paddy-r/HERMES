import json
import pickle
import os
import pandas as pd
from hermes import utilities as hutils
from hermes.regressions.base import RegressionModel
from hermes.constants import WAVE_DATA_PREFIX, WAVE_DATA_SUFFIX, REGRESSION_LAG

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

        lag = self.spec.get(
            "lag",
            REGRESSION_LAG
        )

        if lag < 0:
            raise ValueError(
                f"Regression lag < 0 "
                f"not allowed; replace with lag => 0."
            )

        if lag > 1:
            print(
                f"Warning: regression lag = {lag}. "
                f"This model will estimate relationships "
                f"across {lag} waves rather than a single-wave "
                f"transition. Coefficients may therefore require "
                f"additional interpretation. If single-wave "
                f"coefficients are preferred, consider generating "
                f"or imputing intermediate waves (e.g. with "
                f"hermes-impute) and using lag = 1 instead."
            )

        if (
                lag == 0
                and
                self.spec["response"]
                in self.spec["predictors"]
        ):
            raise ValueError(
                "Response variable may not also "
                "appear in predictors when "
                "lag = 0."
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

        if len(wave_files) < (
                minimum_waves + lag - 1
        ):
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

    def prepare_training_dataset(
            self,
            regression,
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

        lag = self.spec.get(
            "lag",
            REGRESSION_LAG
        )

        for i in range(
                len(wave_files) - lag
        ):
            predictor_file = wave_files[i]

            response_file = wave_files[i + lag]

            print(
                f"{predictor_file} "
                f"-> "
                f"{response_file}"
            )

            predictor_wave = pd.read_csv(
                os.path.join(
                    data_path,
                    predictor_file
                )
            )

            response_wave = pd.read_csv(
                os.path.join(
                    data_path,
                    response_file
                )
            )

            if uid_column is None:

                merged = pd.concat(
                    [
                        predictor_wave.add_suffix("_predictor"),
                        response_wave.add_suffix("_response")
                    ],
                    axis=1
                )

            else:

                merged = predictor_wave.merge(
                    response_wave,
                    on=uid_column,
                    suffixes=(
                        "_predictor",
                        "_response"
                    )
                )

            pair_training_data = (
                regression.create_training_dataset(
                    merged=merged,
                    predictors=self.spec["predictors"],
                    response=self.spec["response"]
                )
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
                    len(wave_files) - lag
            )
            * len(predictor_wave)
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

            "lag": self.spec.get(
                "lag",
                REGRESSION_LAG
            ),

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
            self.prepare_training_dataset(
                regression,
                data_path,
                wave_files
            )
        )

        # print(
        #     training_data[
        #         RegressionModel.RESPONSE_COLUMN
        #     ].value_counts()
        # )
        #
        # print(
        #     training_data.groupby("education")
        #     [RegressionModel.RESPONSE_COLUMN]
        #     .mean()
        # )

        X = training_data[
            self.spec["predictors"]
        ].to_numpy()

        y = training_data[
            RegressionModel.RESPONSE_COLUMN
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
