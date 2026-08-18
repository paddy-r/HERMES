import numpy as np
from hermes.sources.base import FunctionalForm


class Exponential(FunctionalForm):

    def evaluate(self, domains):

        x = domains[self.domains[0]]
        c, a, b = self.parameters
        return c + a * np.exp(b * x)
