# HR 10/02/26 All abstract classes and utility methods/functions


class Agent:
    """Simple container for population units."""
    def __init__(self, domains: dict):
        self.domains = domains

    def __repr__(self):
        return f"<Agent {self.domains}>"
