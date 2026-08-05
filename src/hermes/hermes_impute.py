# HR 03/08/26 Run imputation model on existing data
import argparse
import hermes.engine
import hermes.utilities as hutils


DEFAULTS = {
    "signature": True,
    # "dump": True,
}


def run_imputation(spec: dict):

    if spec["signature"]:
        hutils.print_signature()

    spec.pop("signature")

    print("### Running HERMES imputation ###")
    print(f"Universe: {spec['universe']}")
    print(f"Config: {spec['config']}")
    print(f"Imputation type: {spec['imputation']}")

    imputation = hermes.engine.Imputation(spec=spec)
    imputation.verify()
    imputation.run()


def main():

    parser = argparse.ArgumentParser(
        description="HERMES imputation model specification parser",
    )

    parser.add_argument(
        "-u",
        "--universe",
        type=str,
        dest="universe",
        default="core",
        help="HERMES universe: specifies a folder containing data and config (default: core)",
    )

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        dest="config",
        help="HERMES model config: specifies input data source",
    )

    parser.add_argument(
        "-i",
        "--imputation",
        required=True,
        type=str,
        dest="imputation",
        help="HERMES imputation model type to be computed",
    )

    parser.add_argument(
        "-p",
        "--predictors",
        required=True,
        type=str,
        nargs="+",
        dest="predictors",
        help="HERMES imputation model predictors",
    )

    parser.add_argument(
        "-t",
        "--target",
        required=True,
        type=str,
        dest="target",
        help="HERMES imputation target variable",
    )

    parser.add_argument(
        "-s",
        "--signature",
        required=False,
        type=str,
        dest="signature",
        default=DEFAULTS["signature"],
        help="Show HERMES signature at runtime",
    )

    # parser.add_argument(
    #     "-d",
    #     "--dump",
    #     required=False,
    #     type=str,
    #     dest="dump",
    #     default=DEFAULTS["dump"],
    #     help="Output imputed data",
    # )

    args = parser.parse_args()
    hermes_spec = vars(args)
    run_imputation(hermes_spec)


if __name__ == "__main__":
    main()


    # # Testing without argparse
    # spec = DEFAULTS | {
    #     'universe': 'core',
    #     'config': 'time',
    #     'imputation': '',
    #     'predictors': '',
    #     'target': '',
    # }
    # run_imputation(spec)