from hermes.regressions.base import RegressionModel
import json
import pickle
import os
import pandas as pd
from hermes import utilities as hutils


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

    def verify(self):

        print(
            "Verifying Regression model handler"
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

        regression_name = (
            REGRESSION_ALIASES.get(
                self.spec["regression"],
                self.spec["regression"]
            )
        )

        regression_class = (
            RegressionModel.registry[
                regression_name
            ]
        )

        print(
            f"Selected regression model: "
            f"{regression_class.__name__}"
        )

        regression = regression_class()

        print(
            regression
        )

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

        data_path = (
            hutils.get_latest_by_config(
                universe=self.spec["universe"],
                config=self.spec["config"]
            )
        )

        print(
            f"Training data path:\n"
            f"{data_path}"
        )

        step_files = sorted(
            [
                file
                for file in os.listdir(
                    data_path
                )
                if file.startswith(
                    "step"
                )
                and file.endswith(
                    ".csv"
                )
            ]
        )

        print(
            f"Found "
            f"{len(step_files)} "
            f"step files"
        )

        wave0 = pd.read_csv(
            os.path.join(
                data_path,
                step_files[0]
            )
        )

        wave1 = pd.read_csv(
            os.path.join(
                data_path,
                step_files[1]
            )
        )

        print(
            "Wave 0 shape:",
            wave0.shape
        )

        print(
            "Wave 1 shape:",
            wave1.shape
        )

        training_data = wave0[
            self.spec["predictors"]
        ].copy()

        # Temporary: response is predictor[0] measured in the next wave

        training_data[
            self.spec["response"]
        ] = wave1[
            self.spec["predictors"][0]
        ]

        print(
            "Training dataset shape:",
            training_data.shape
        )

        print(
            training_data.head()
        )

        print(
            training_data.describe()
        )

        print(
            training_data.corr(
                numeric_only=True
            )
        )

        X = training_data[
            self.spec["predictors"]
        ]

        y = training_data[
            self.spec["response"]
        ]

        fit_results = regression.fit(
            X,
            y
        )

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
