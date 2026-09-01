import os
import numpy as np
import pandas as pd
import pickle
import json
from hermes.sources.base import Source
from hermes.constants import REGRESSION_LAG

class RegressionSource(Source):

    @property
    def regression_type(self):
        return self.metadata.get(
            "regression_type"
        )

    @property
    def predictors(self):
        return self.metadata.get(
            "predictors",
            []
        )

    @property
    def response(self):
        return self.metadata.get(
            "response"
        )

    @property
    def lag(self):
        return self.metadata.get(
            "lag",
            REGRESSION_LAG
        )

    def __init__(
        self,
        config,
        inpath
    ):

        self.config = config
        self.inpath = inpath

        print(
            "Initialising RegressionSource"
        )

        print(
            f"Model specified: "
            f"{config['model']}"
        )

        if "model_path" in config:

            basepath = os.path.join(
                config["model_path"],
                config["model"]
            )

        else:

            basepath = os.path.join(
                self.inpath,
                "regressions",
                config["model"]
            )

        print(
            f"Resolved model path:\n"
            f"{basepath}"
        )

        model_path = (
                basepath + ".pkl"
        )

        metadata_path = (
                basepath + ".json"
        )

        with open(
                model_path,
                "rb"
        ) as f:
            self.model = pickle.load(
                f
            )

        with open(
                metadata_path
        ) as f:
            self.metadata = json.load(
                f
            )

        print(
            f"Loaded regression model:"
        )

        print(
            self.model,
            self.model.__class__.__name__
        )

        print(
            "Loaded regression metadata:"
        )

        print(
            self.metadata
        )

    def verify(self):

        print(
            "Verifying RegressionSource"
        )

    def predict(
            self,
            X
    ):

        return self.model.predict(
            X
        )

    def predict_proba(
            self,
            X
    ):
        return self.model.predict_proba(
            X
        )

    def evaluate(
            self,
            domains
    ):

        predictors = np.array(
            [domains]
        )

        prediction = (
            self.model.predict(
                predictors
            )[0]
        )

        return prediction
