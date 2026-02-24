# HR 10/02/26 All utility functions
import hermes
import os
from os.path import dirname as up
import datetime

JOIN_CHARACTER = '__'
INPATH_DEFAULT = os.path.join(up(up(up(hermes.__file__))), "universes")
OUTPATH_DEFAULT = os.path.join(up(up(up(hermes.__file__))), "output")
PRIORITY_MISSING_DEFAULT = -1

def print_signature() -> None:
    fullpath = os.path.join(up(__file__), "signature.txt")
    with open(fullpath) as f:
        print(f.read(), "\n")

def get_timestamp() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp

def get_output_path(universe: str, config: str, upper_path: str=OUTPATH_DEFAULT, join_character: str=JOIN_CHARACTER) -> str:
    timestamp = get_timestamp()
    output_path = join_character.join([timestamp, universe, config])
    full_path = os.path.join(upper_path, output_path)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)
    return full_path

def get_input_path(universe: str, upper_path: str=INPATH_DEFAULT) -> str:
    full_path = os.path.join(upper_path, universe)
    return full_path

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
