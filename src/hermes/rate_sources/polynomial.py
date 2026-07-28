import numpy as np
from hermes.base_classes import FunctionalForm


class Polynomial(FunctionalForm):

    name = "polynomial"

    def __init__(self, parameters):
        self.parameters = parameters

    def evaluate(self, x):
        return np.polyval(self.parameters, x)
    