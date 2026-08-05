from abc import ABC, abstractmethod
import pandas as pd
from hermes.rate_sources.base import FunctionalForm
from hermes.rate_sources.rate_table import RateTable
from hermes.engine.population import Population
import os


class TransitionModel(ABC):

    registry = {}
    creates_domains = {}
    # input_domains = []

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        TransitionModel.registry[
            cls.__name__
        ] = cls

    def __init__(self, attrs):

        self.attrs = attrs
        self.inpath = attrs.get("inpath")
        self.priority = attrs.get(
            "priority",
            0
        )

        self.rate_source = None
        if "rate_source" in attrs:

            self.rate_source = (
                self.build_rate_source(
                    attrs["rate_source"]
                )
            )


    def build_rate_source(self, config):

        source_type = config["type"]
        if source_type == "function":

            function_class = (
                FunctionalForm.registry[
                    config["function"]
                ]
            )

            # return function_class(
            #     domains=config["domains"],
            #     parameters=config["parameters"]
            return function_class(**config)

        elif source_type == "rate_table":

            fullpath = os.path.join(
                self.inpath,
                config["file"]
            )
            table = pd.read_csv(fullpath)

            return RateTable(table)

        raise ValueError(
            f"Unknown rate source type: {source_type}"
        )

    @abstractmethod
    def apply_transition(self, population):
        pass


### 29/07/26 Dumping this here for future
class TransitionModelOld(ABC):
    """Prototype for all transition models."""
    def __init__(self, attrs: dict):
        self.attrs = attrs
        # self.required = self.attrs.get("required", [])  # Get required domains (i.e. variables)
        if "rate_table" in self.attrs:
            self.rate_table = self.attrs["rate_table"]
            self.rate_domains = [col for col in self.rate_table.columns if col != "value"]
            self.rate_dict = self.rate_table.groupby(self.rate_domains)["value"].mean().to_dict()  # Mean is workaround

    def __repr__(self):
        # return f"<TransitionModel {self.__class__.__name__},\n  required domains: {self.required}>"
        return f"<TransitionModel {self.__class__.__name__}"

    def apply_probability(self, population: Population) -> Population:
        """Apply probabilistic or matrix-based transform to domain(s)."""
        return population

    def apply_transition(self, population: Population) -> Population:
        """Mutate the domain(s) in any way not possible with a probabilistic method."""
        # print(f"Running {self.__class__.__name__}")
        return population
