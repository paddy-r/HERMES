# HR 10/02/26 All utility functions
import hermes
import os
from os.path import dirname as up
import datetime
import pandas as pd
from string import ascii_lowercase as alphabet

JOIN_CHARACTER = '__'
INPATH_DEFAULT = os.path.join(up(up(up(hermes.__file__))), "universes")
OUTPATH_DEFAULT = os.path.join(up(up(up(hermes.__file__))), "output")
PRIORITY_MISSING_DEFAULT = -1

UKHLS_DATA_PATH = os.path.join(up(up(up(up(up(__file__))))), "data", "UKDA-6614-stata", "stata", "stata13_se", "ukhls")
BHPS_DATA_PATH = os.path.join(up(up(up(up(up(__file__))))), "data", "UKDA-6614-stata", "stata", "stata13_se", "bhps")


def print_signature() -> None:
    fullpath = os.path.join(up(__file__), "signature.txt")
    with open(fullpath) as f:
        print(f.read(), "\n")

def get_timestamp() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp

def ensure_directory(full_path: str) -> str:
    if not os.path.isdir(full_path):
        os.makedirs(full_path)
    return full_path

def get_output_path(universe: str, config: str, upper_path: str=OUTPATH_DEFAULT, join_character: str=JOIN_CHARACTER) -> str:
    timestamp = get_timestamp()
    output_path = join_character.join([timestamp, universe, config])
    full_path = os.path.join(upper_path, output_path)
    full_path = ensure_directory(full_path)
    return full_path

def get_input_path(universe: str, upper_path: str=INPATH_DEFAULT) -> str:
    full_path = os.path.join(upper_path, universe)
    return full_path

def get_latest_by_config(universe: str, config: str, outpath: str=OUTPATH_DEFAULT) -> str:
    universe_fullname = JOIN_CHARACTER + universe + JOIN_CHARACTER
    _path = sorted([el for el in os.listdir(outpath) if universe_fullname in el and el.endswith(config)])[-1]
    fullpath = os.path.join(outpath, _path)
    return fullpath

def resolve_transition_priorities(transitions: list) -> list:
    """Parse and order transition model priorities as follows:
     1. First, order by any priorities stated in transitions list, then
     2. For any models without priorities, append by order they appear in transitions list"""
    order_raw = [(model_dict.get("name"), model_dict.get("priority", PRIORITY_MISSING_DEFAULT)) for model_dict in transitions]
    first = [el for el in order_raw if el[1] != PRIORITY_MISSING_DEFAULT]
    second = [el for el in order_raw if el[1] == PRIORITY_MISSING_DEFAULT]
    order = [el[0] for el in sorted(first, key=lambda x: x[1])] + [el[0] for el in second]
    return order

def flatten(lol: list) -> list:
    flat = []
    for l in lol:
        flat.extend(l)
    return flat

def get_ukhls_prefix(year):
    """Get wave letter based on year for US data.

    Waves 1990-2008 are waves A-R of BHPS, 2009 onwards are UKHLS.

    Examples
    --------
    For year 1992 this will return wave string "c".

    Parameters
    ----------
    year : int
        Year of survey.
    Returns
    -------
    wave_letter : str
        Letter that corresponds to wave.
    """
    # BHPS/UKHLS naming convention, with BHPS beginning with "b" in all cases, then both with "a_", "b_" etc.
    if year < 2009:
        wave_number = year - 1991
    else:
        wave_number = year - 2008
    wave_letter = alphabet[wave_number]
    if year < 2009:
        wave_letter = "b" + wave_letter
    return wave_letter

def get_ukhls_data(year, dataset):
    """Retrieve UKHLS/BHPS data from adjacent folder for specified year and dataset type."""
    year_prefix = get_ukhls_prefix(year)
    if year < 2009:
        data_path = BHPS_DATA_PATH
    else:
        data_path = UKHLS_DATA_PATH
    dataset_filename = year_prefix + "_" + dataset + ".dta"
    dataset_fullpath = os.path.join(data_path, dataset_filename)
    data = pd.read_stata(dataset_fullpath, convert_categoricals=False)
    return data
