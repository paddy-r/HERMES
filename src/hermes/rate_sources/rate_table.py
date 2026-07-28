from hermes.base_classes import RateSource


class RateTable(RateSource):

    def __init__(self, table):
        self.table = table

    def evaluate(self, domains):
        """DO SOMETHING HERE"""
        pass
