# HR 10/08/26 Universe management utility
import argparse
import os
import shutil
from hermes import utilities as hutils


UNIVERSE_SUBDIRECTORIES = [
    "configs",
    "populations",
    "transitions",
    "regressions",
    "imputations",
    "persistent_data",
    "rate_tables",
]


def create_universe(universe_name: str):

    response = input(
        f"Create universe '{universe_name}'? (y/n): "
    )

    if response.lower() != "y":
        print("Cancelled.")
        return

    universe_path = os.path.join(
        hutils.INPATH_DEFAULT,
        universe_name
    )

    os.makedirs(
        universe_path,
        exist_ok=True
    )

    for directory in UNIVERSE_SUBDIRECTORIES:

        os.makedirs(
            os.path.join(
                universe_path,
                directory
            ),
            exist_ok=True
        )

    print(
        f"Created universe:\n{universe_path}"
    )


def delete_universe(
        universe_name: str
):

    response = input(
        f"Delete universe '{universe_name}'? (y/n): "
    )

    if response.lower() != "y":
        print("Cancelled.")
        return

    universe_path = os.path.join(
        hutils.INPATH_DEFAULT,
        universe_name
    )

    shutil.rmtree(
        universe_path
    )

    print(
        f"Deleted universe:\n{universe_path}"
    )


def main():

    parser = argparse.ArgumentParser(
        description="HERMES universe management utility",
    )

    parser.add_argument(
        "-c",
        "--create",
        type=str,
        dest="create",
        help="Create a new universe",
    )

    parser.add_argument(
        "-d",
        "--delete",
        type=str,
        dest="delete",
        help="Delete an existing universe",
    )

    args = parser.parse_args()

    if args.create:

        create_universe(
            args.create
        )

    elif args.delete:

        delete_universe(
            args.delete
        )

    else:

        parser.print_help()


if __name__ == "__main__":
    main()