# HR 10/02/26 All abstract classes and utility methods/functions
import sys
import os
import json
from abc import ABC
import hermes.utilities as hutils
import pandas as pd
import importlib


class Simulation:
    """Prototype for all simulations."""
    def __repr__(self):
        return f"<Simulation {self.spec}>"

    def __init__(self, spec: dict):
        self.spec = spec
        universe = self.spec["universe"]
        config = self.spec["config"]
        self.dump = self.spec["dump"]

        # 1. Get/check output folder
        self.outpath = hutils.get_output_path(universe=universe, config=config)

        # 2. Read in run spec
        self.inpath = hutils.get_input_path(universe=universe)
        if not os.path.isdir(self.inpath):
            print("Universe input path does not exist; stopping")
            return

        # 3. Get config and population files
        config_file = os.path.join(self.inpath, config + '.json')
        with open(config_file, 'r') as f:
            run_config = json.load(f)
            self.spec.update(run_config)  # Add all parameters in config file to spec

        # 4. Load population data
        population_file = os.path.join(self.inpath, spec['population'])
        population_data = pd.read_csv(population_file)
        self.population = Population(data=population_data)

        # 5. Resolve transition model priorities, then import each dynamically + instantiate
        sys.path.insert(0, self.inpath)
        transitions_module = importlib.import_module("transitions")
        self.model_order = hutils.resolve_transition_priorities(self.spec["transitions"])
        transition_attrs = {_dict["name"]: _dict.get("params", {}) for _dict in self.spec["transitions"]}  # Get all runtime parameters
        transition_rate_tables = {_dict["name"]: os.path.join(self.inpath, _dict["rate_table"]) for _dict in self.spec["transitions"] if "rate_table" in _dict}  # Get rate table full paths, if present
        for model, rate_table in transition_rate_tables.items():
            transition_attrs[model]["rate_table"] = pd.read_csv(rate_table)
        self.models = [getattr(transitions_module, model)(transition_attrs[model]) for model in self.model_order]  # getattr instantiates each transition model

        # 6. Check all required domains (as specified in transitions) are present in input population
        transition_requirements = set(hutils.flatten([_dict.get("required", []) for _dict in self.spec["transitions"]]))
        population_domains = set(self.population.data.columns)
        print("\nDomains required for transition models that are not present in input population:")
        print(transition_requirements - population_domains)

    def type_check(self, domains: list):
        return

    def save_population(self, step_number):
        pop_file = "step" + str(step_number) + ".csv"
        fullpath = os.path.join(self.outpath, pop_file)
        self.population.data.to_csv(fullpath, index=False)

    def run(self):
        print("\nRunning simulation with spec:\n{}".format(self.spec))

        # Save input population
        if self.dump:
            self.save_population(step_number=0)

        n_steps = self.spec["steps"]
        for i in range(n_steps):
            print("\n## Running step {} of {}".format(i+1, n_steps))
            for j, model in enumerate(self.models):
                self.models[j].apply_transition(self.population)
            if self.dump:
                self.save_population(step_number=i+1)


class Agent:
    """Simple container for population units."""
    def __init__(self, domains: dict):
        self.domains = domains

    def __repr__(self):
        return f"<Agent {self.domains}>"


class Population:
    """Simple container for populations; variables are referred to as domains."""
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __repr__(self):
        return f"<Population {self.data}>"


class TransitionModel(ABC):
    """Prototype for all transition models."""
    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.required = self.attrs.get("required", [])  # Get required domains (i.e. variables)
        if "rate_table" in self.attrs:
            self.rate_table = self.attrs["rate_table"]
            self.rate_domains = [col for col in self.rate_table.columns if col != "value"]
            self.rate_dict = self.rate_table.groupby(self.rate_domains)["value"].mean().to_dict()  # Mean is workaround

    def __repr__(self):
        return f"<TransitionModel {self.__class__.__name__},\n  required domains: {self.required}>"

    def apply_probability(self, population: Population) -> Population:
        """Apply probabilistic or matrix-based transform to domain(s)."""
        return population

    def apply_transition(self, population: Population) -> Population:
        """Mutate the domain(s) in any way not possible with a probabilistic method."""
        # print(f"Running {self.__class__.__name__}")
        return population
