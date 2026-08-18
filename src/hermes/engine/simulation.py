# HR 29/07/26 Simulation engine classes, moved from earlier common script to its own
import os
import json
import pandas as pd
import hermes.utilities as hutils
from .population import Population
import hermes.verification
from hermes.verification.base import Verifier
from hermes.constants import WAVE_DATA_PREFIX


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
        self.inpath = hutils.get_universe_path(universe=universe)

        if not os.path.isdir(
                self.inpath
        ):
            print(
                "Universe input path does not exist; stopping"
            )
            return

        # 3. Get config and population files
        config_file = os.path.join(
            self.inpath,
            "configs",
            config + '.json',
        )
        with open(config_file, 'r') as f:
            run_config = json.load(f)
            self.spec.update(run_config)  # Add all parameters in config file to spec

        for transition in self.spec["transitions"]:
            transition["inpath"] = self.inpath

        # 4. Load population data
        population_file = os.path.join(
            self.inpath,
            "populations",
            spec['population'],
        )
        population_data = pd.read_csv(population_file)

        population_structure = spec.get(
            "population_structure",
            {}
        )
        self.population = Population(
            data=population_data,
            structure=population_structure,
        )

        # 5. Resolve transition model priorities, then import each dynamically + instantiate
        import hermes.transitions
        from hermes.transitions.base import (
            TransitionModel
        )

        ### Removed for now, but want to reinstate universe-specific models later
        # sys.path.insert(0, self.inpath)
        # transitions_module = importlib.import_module("transitions")

        self.model_order = hutils.resolve_transition_priorities(
            self.spec["transitions"]
        )

        transition_attrs = {
            _dict["name"]: _dict
            for _dict in self.spec["transitions"]
        }

        self.models = []
        for model in self.model_order:
            if model in TransitionModel.registry:

                model_class = (
                    TransitionModel.registry[model]
                )

            self.models.append(
                model_class(
                    transition_attrs[model]
                )
            )

    def verify(self):

        print("Verifying configuration...")

        verifiers = sorted(Verifier.registry.values(),
                           key=lambda x: x.priority)

        for verifier in verifiers:
            verifier().verify(self)


    def save_population(self, wave_number):
        pop_file = hutils.get_wave_filename(
            wave_number
        )
        fullpath = os.path.join(self.outpath, pop_file)
        self.population.data.to_csv(fullpath, index=False)

    def run(self):
        print("\nRunning simulation with spec:\n{}".format(self.spec))

        # Save input population
        if self.dump:
            self.save_population(wave_number=0)

        n_steps = self.spec["steps"]
        for i in range(n_steps):
            print("\n## Running step {} of {}".format(i+1, n_steps))
            for j, model in enumerate(self.models):
                self.models[j].apply_transition(self.population)
            if self.dump:
                self.save_population(wave_number=i+1)

