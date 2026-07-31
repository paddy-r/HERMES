import numpy as np
from hermes.rate_sources.base import FunctionalForm


class Gaussian(FunctionalForm):

    def evaluate(self, domains):

        x = domains[self.domains[0]]
        a, mu, sigma = self.parameters
        return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

