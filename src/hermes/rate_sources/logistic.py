import numpy as np
from hermes.rate_sources.base import FunctionalForm


class Logistic(FunctionalForm):

    def evaluate(self, domains):

        x = domains[self.domains[0]]
        el, k, x0 = self.parameters
        return el / (1 + np.exp(-k * (x - x0)))
