import numpy as np
from hermes.base_classes import FunctionalForm


class Exponential(FunctionalForm):

    name = "exponential"

    def __init__(self, parameters):
        self.a, self.b = parameters

    def evaluate(self, x):
        return self.a * np.exp(self.b * x)
    