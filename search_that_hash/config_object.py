import toml
from appdirs import *
import json

from name_that_hash import runner as nth

import logging
import coloredlogs


def read_config_file():
    return read_and_parse_config_file(find_appdirs_location())


def find_appdirs_location():
    # TODO make this OS independent the "/" makes it Windows specific
    # print(user_config_dir("HashSearch", "Bee-san") + "/config.toml")
    pass
    # TODO where does this function exist lol
    # return user_config_dir("HashSearch", "Bee-san") + "/config.toml"


def read_and_parse_config_file(file):
    config_to_parse = read_file(file)

    if config_to_parse == None:
        return config_to_parse
    else:
        try:
            return toml.loads(config_to_parse)
        except:
            return None


def read_file(file):
    try:
        with open(file, "r") as out:
            return out.read()
    except:
        return None


def cli_config(kwargs):

    config = default_config()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        logging.debug("Hashes are from file")
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    config["hashes"] = create_hash_config(config["hashes"])
    config.update(kwargs)

    logging.info("Returning config")
    return config


def api_config(hashes: str, sth_api: str = None):
    config = default_config()
    config["hashes"] = create_hash_config(hashes)
    config["api"] = True
    if not sth_api:
        config["api_keys"]["STH"] = sth_api
    return config


def default_config():
    return {
        "api_keys": {"STH": "rGFbPbSXMF5ldzid2eyA81i6aCa497Z25MNgi8sa"},
        "hashcat": False,
        "api": False,
        "greppable": False,
        "hashes": None,
        "hashcat_binary": None,
        "timeout": 1,
        "wordlist": None,
        "offline": False,
    }


def create_hash_config(hashes):
    # Gets the results from name-that-hash
    logging.debug("Called NTH to get hash types")
    nth_result_types = json.loads(nth.api_return_hashes_as_json(hashes))
    return nth_result_types
