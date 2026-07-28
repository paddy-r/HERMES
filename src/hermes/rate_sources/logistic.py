import numpy as np
from hermes.base_classes import FunctionalForm


class Logistic(FunctionalForm):

    name = "logistic"

    def __init__(self, parameters):
        self.L, self.k, self.x0 = parameters

    def evaluate(self, x):
        return self.L / (
            1 + np.exp(
                -self.k * (x - self.x0)
            )
        )
    