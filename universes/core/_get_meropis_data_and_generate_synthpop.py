# HR 27/03/26 To grab data from Meropis demonstrator and recreate artificial population in HERMES folders
# and to create config dictionary (by reading default config file and overwriting with spec) for full automation

import subprocess
import json
import os
from os.path import dirname as up
import pandas as pd
import zipfile

COMPASS_PATH = os.path.join(up(up(up(up(__file__)))), "COMPASS-main")
COMPASS_BINARY_PATH = os.path.join(COMPASS_PATH, "COMPASS")
COMPASS_DEFAULT_CONFIG_FILE = "config.json"
CURRENT_PATH = up(__file__)


def run_compass(config_dict, binary_path=COMPASS_BINARY_PATH):
    """
    Run COMPASS from Python with a configuration dictionary.

    Args:
        config_dict: Dictionary containing COMPASS configuration parameters
        binary_path: Path to compiled COMPASS binary

    Returns:
        Dictionary with results including status, message, and log
    """
    # Convert to compact JSON
    config_json = json.dumps(config_dict, separators=(',', ':'), ensure_ascii=False)

    try:
        # Execute COMPASS
        result = subprocess.run(
            [binary_path],
            input=config_json,
            capture_output=True,
            text=True,
            check=False
        )

        # Parse JSON response
        if result.stdout:
            response = json.loads(result.stdout)
        else:
            response = {"status": "error", "message": "No output from COMPASS"}

        # Add execution details
        response["return_code"] = result.returncode
        if result.stderr:
            response["stderr"] = result.stderr.splitlines()

        return response

    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": f"Failed to parse COMPASS output: {str(e)}",
            "raw_output": result.stdout if 'result' in locals() else None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to execute COMPASS: {str(e)}"
        }


if __name__ == "__main__":

    # 1. Get default config from COMPASS, so optimisation parameters are all there
    config_default_fullpath = os.path.join(COMPASS_PATH, COMPASS_DEFAULT_CONFIG_FILE)
    with open(config_default_fullpath, 'r') as config:
        config_dict = json.load(config)

    # 2. Specify all file names/paths - want to dump everything necessary for microsim in folder here
    constraints = os.path.join(COMPASS_PATH, "data", "BlockWorld", "artifical_cencus.csv")
    microdata_hh = os.path.join(COMPASS_PATH, "data", "BlockWorld", "artifical_survey.csv")
    microdata_ind = os.path.join(COMPASS_PATH, "data", "BlockWorld", "compleate_artifical_individual_survey.csv")
    groups = os.path.join(COMPASS_PATH, "data", "BlockWorld", "artificial_groups.csv")

    synthpop_bare = os.path.join(CURRENT_PATH, "input_data", "synthetic_population_bare.csv")
    validation = os.path.join(CURRENT_PATH, "input_data", "synthetic_population_validation.csv")
    microdata_ind_out = os.path.join(CURRENT_PATH, "input_data", "microdata_ind.csv")
    sp_out = os.path.join(CURRENT_PATH, "populations/population.csv")

    # 2a. Overwrite config fields as necessary
    config_dict_updates = {
        "constraints": constraints,
        "microdata": microdata_hh,
        "groups": groups,
        "output": synthpop_bare,
        "validate": validation,
    }
    config_dict |= config_dict_updates

    # 3. Run COMPASS remotely, passing config
    result = run_compass(config_dict=config_dict)

    # 4. Print result/errors with stdout
    print("Status:", result.get("status"))
    print("Message:", result.get("message"))

    if "log" in result:
        print("\nExecution Log:")
        for line in result["log"]:
            print(f"  {line}")

    # 5. Copy/move ind-level microdata so everything in one place here
    md_ind_in = pd.read_csv(microdata_ind)
    md_ind_in.to_csv(microdata_ind_out, index=False)
    del md_ind_in

    # 6. Populate synthpop with individual-level data
    sp_bare_to_drop = []
    md_ind_to_drop = ["area", "admin_area", "in_household"]
    sp_to_drop = ["microdata_id"]

    sp_bare = pd.read_csv(synthpop_bare).drop(columns=sp_bare_to_drop)
    md_ind = pd.read_csv(microdata_ind_out).drop(columns=md_ind_to_drop)
    sp = sp_bare.merge(md_ind, how="outer", left_on="microdata_id", right_on="household_id").drop(columns=sp_to_drop)
    sp.to_csv(sp_out, index=False)
