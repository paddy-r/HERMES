from abc import ABC, abstractmethod


class RateSource(ABC):

    @abstractmethod
    def evaluate(self, domains):
        pass


class FunctionalForm(RateSource):

    registry = {}

    def __init__(self, domains, parameters, **kwargs):

        self.domains = domains
        self.parameters = parameters

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        FunctionalForm.registry[
            cls.__name__.lower()
        ] = cls
