import numpy as np
from hermes.base_classes import FunctionalForm


class Power(FunctionalForm):

    name = "power"

    def __init__(self, parameters):
        self.a, self.b = parameters

    def evaluate(self, x):
        return self.a * np.power(x, self.b)
    
