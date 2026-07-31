# HR 29/07/26 Population classes, moved from earlier common script to its own
import pandas as pd


class Population:
    """Simple container for populations; variables are referred to as domains."""
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __repr__(self):
        return f"<Population {self.data}>"
