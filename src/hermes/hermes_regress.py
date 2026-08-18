# HR 03/08/26 Run regression model on existing data
import argparse
import hermes.engine
import hermes.utilities as hutils

DEFAULTS = {"signature": True,
            # "dump": True,
            }


def run_regression(spec: dict):
    if spec["signature"]:
        hutils.print_signature()  # Print HERMES signature if specified
    spec.pop("signature")

    print("### Running HERMES regression ###")
    print(f"Universe: {spec["universe"]}")
    print(f"Config: {spec["config"]}")
    print(f"Regression type: {spec["regression"]}")

    regression = hermes.engine.Regression(spec=spec)
    regression.verify()
    regression.run()

def main():
    parser = argparse.ArgumentParser(description="HERMES regression model specification parser",
                                     )

    parser.add_argument("-u", "--universe", type=str, dest='universe', default='core',
                        help="HERMES universe: specifies a folder containing data and config (default: core)",
                        )
    parser.add_argument("-c", "--config", required=True, type=str, dest='config',
                        help="HERMES model config: specifies input population and transition models",
                        )
    parser.add_argument("-r", "--regression", required=True, type=str, dest='regression',
                        help="HERMES model config: specifies regression model type to be computed",
                        )
    parser.add_argument("-p", "--predictors", required=True, type=str, nargs="+", dest='predictors',
                        help="HERMES model config: specifies regression model predictors",
                        )
    parser.add_argument("-e", "--response", required=True, type=str, dest='response',
                        help="HERMES model config: specifies regression model response",
                        )
    parser.add_argument("-s", "--signature", required=False, type=str, dest='signature',
                        help="Show HERMES signature at runtime", default=DEFAULTS["signature"],
                        )
    parser.add_argument(
        "--uid",
        type=str,
        dest="uid",
        default=None,
        help="Persistent unique ID (UID) used to match units across waves"
    )
    parser.add_argument(
        "--group",
        action="store_true",
        dest="group",
        help="Train grouped regression model (e.g. household-level model)"
    )
    parser.add_argument(
        "--training_path",
        dest="training_path",
        help="Path containing wave CSV files for training."
             "Currently, -u and -c remain mandatory even when training_path is specified."
             "This behaviour may be relaxed in a future release."
    )

    args = parser.parse_args()
    hermes_spec = vars(args)  # Convert to dictionary
    run_regression(hermes_spec)


if __name__ == "__main__":
    main()


    # # Testing without argparse
    # spec = DEFAULTS | {
    #     'universe': 'core',
    #     'config': 'time_stochastic_regression',
    #     'regression': 'linear',
    #     'predictors': '',
    #     'response': '',
    # }
    # run_regression(spec)
