import numpy as np
from hermes.base_classes import FunctionalForm


class Gaussian(FunctionalForm):

    name = "gaussian"

    def __init__(self, parameters):
        self.a, self.mu, self.sigma = parameters

    def evaluate(self, x):
        return self.a * np.exp(
            -((x - self.mu) ** 2)
            / (2 * self.sigma ** 2)
        )
