import numpy as np
from hermes.sources.base import FunctionalForm


class Polynomial(FunctionalForm):

    def evaluate(self, domains):

        x = domains[self.domains[0]]
        return np.polyval(self.parameters, x)
