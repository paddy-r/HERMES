import numpy as np
from hermes.rate_sources.base import FunctionalForm


class Power(FunctionalForm):

    def evaluate(self, domains):

        x = domains[self.domains[0]]
        a, b = self.parameters
        return a * np.power(x, b)
