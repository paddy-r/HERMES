# HR 05/02/26 Run script
import argparse

def run_with_config(config):
    print("Running HERMES with config:\n {}".format(config))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="HERMES specification parser",
                                     )

    parser.add_argument("-c", "--config", required=True, type=str, dest='config',
                        help="Model config",
                        )

    args = parser.parse_args()
    hermes_config = args.config
    run_with_config(hermes_config)
