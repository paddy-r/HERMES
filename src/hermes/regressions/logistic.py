from sklearn.linear_model import LogisticRegression
from hermes.regressions.base import RegressionModel
import pandas as pd


class LogisticRegressionModel(RegressionModel):

    minimum_waves = 2

    def __init__(self):

        self.model = (
            LogisticRegression(
                max_iter=1000
            )
        )

    def transform_response(
            self,
            predictor_wave,
            response_wave
    ):
        return (
                response_wave > predictor_wave
        ).astype(int)

    def fit(
            self,
            X,
            y
    ):

        self.model.fit(
            X,
            y
        )

        print(
            "Coefficients:"
        )

        print(
            self.model.coef_
        )

        print(
            "Intercept:"
        )

        print(
            self.model.intercept_
        )

    def predict_proba(
            self,
            X
    ):

        return self.model.predict_proba(
            X
        )

    def get_metadata(self):

        return {
            "coefficients":
                self.model.coef_.tolist(),

            "intercept":
                self.model.intercept_.tolist()
        }
