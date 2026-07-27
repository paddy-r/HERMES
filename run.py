# HR 05/02/26 Run script
import argparse
import hermes.base_classes
import hermes.utilities as hutils

DEFAULTS = {"signature": True,
            "dump": True,
            }


def run_with_config(spec: dict):
    if spec["signature"]:
        hutils.print_signature()  # Print HERMES signature if specified
    spec.pop("signature")

    print("### Running HERMES ###")
    print(f"Universe: {spec["universe"]}")
    print(f"Config: {spec["config"]}")

    simulation = hermes.base_classes.Simulation(spec=spec)
    simulation.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="HERMES specification parser",
                                     )

    parser.add_argument("-u", "--universe", type=str, dest='universe', default='core',
                        help="HERMES universe: specifies a folder containing data and config (default: core)",
                        )
    parser.add_argument("-c", "--config", required=True, type=str, dest='config',
                        help="HERMES model config: specifies input population and transition models",
                        )
    parser.add_argument("-s", "--signature", required=False, type=str, dest='signature',
                        help="Show HERMES signature at runtime", default=DEFAULTS["signature"],
                        )
    parser.add_argument("-d", "--dump", required=False, type=str, dest='dump',
                        help="Output population at each step at runtime", default=DEFAULTS["dump"],
                        )

    args = parser.parse_args()
    hermes_spec = vars(args)  # Convert to dictionary
    run_with_config(hermes_spec)


    # # Testing without argparse
    # spec = DEFAULTS | {'universe': 'fertility', 'config': 'config_1'}
    # run_with_config(spec)
