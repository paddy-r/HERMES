import numpy as np
from hermes.sources.base import Source


class RateTable(Source):

    def __init__(self, table):

        self.table = table
        self.domains = [
            col
            for col in table.columns
            if col != "value"
        ]

        self.rate_dict = (
            table
            .groupby(self.domains)["value"]
            .mean()
            .to_dict()
        )

    def evaluate(self, domains):

        n = len(
            domains[self.domains[0]]
        )

        rates = np.zeros(n)

        for i in range(n):

            key = tuple(
                domains[d].iloc[i]
                for d in self.domains
            )

            if len(key) == 1:
                key = key[0]

            rates[i] = self.rate_dict[key]

        return rates
