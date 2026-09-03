from sklearn.linear_model import LinearRegression
from hermes.regressions.base import RegressionModel
import pandas as pd


class LinearRegressionModel(RegressionModel):

    minimum_waves = 2

    def __init__(self):

        self.model = (
            LinearRegression()
        )

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
        #
        # return {
        #     "coefficients":
        #         self.model.coef_.tolist(),
        #
        #     "intercept":
        #         float(self.model.intercept_)
        # }

    def get_metadata(self):
        return {
            "coefficients":
                self.model.coef_.tolist(),

            "intercept":
                float(
                    self.model.intercept_
                )
        }
