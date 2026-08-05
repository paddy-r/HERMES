from sklearn.linear_model import LinearRegression
from hermes.regressions.base import RegressionModel


class LinearRegressionModel(RegressionModel):

    def __init__(self):

        self.model = (
            LinearRegression()
        )

    def get_metadata(self):
        return {
            "coefficients":
                self.model.coef_.tolist(),

            "intercept":
                float(
                    self.model.intercept_
                )
        }

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

        return {
            "coefficients":
                self.model.coef_.tolist(),

            "intercept":
                float(self.model.intercept_)
        }
