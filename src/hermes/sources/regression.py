import os
import numpy as np
import pandas as pd
import pickle
from hermes.sources.base import Source


class RegressionSource(Source):

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

            fullpath = os.path.join(
                config["model_path"],
                config["model"]
            )

        else:

            fullpath = os.path.join(
                self.inpath,
                "regressions",
                config["model"]
            )

        print(
            f"Resolved model path:\n"
            f"{fullpath}"
        )

        with open(
                fullpath,
                "rb"
        ) as f:
            self.model = pickle.load(
                f
            )

        print(
            f"Loaded regression model:"
        )

        print(
            self.model,
            self.model.__class__.__name__
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
