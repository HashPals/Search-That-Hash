from appdirs import *
import json
from loguru import logger

logger.remove()
from name_that_hash import runner as nth

import logging
import coloredlogs
import os.path


def cli_config(kwargs):

    config = default_config()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        logging.debug("Hashes are from file")
        config["hashes"] = "".join(list(kwargs["file"])).strip().split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    config["hashes"] = create_hash_config(config["hashes"])
    config.update(kwargs)

    logging.info("Returning config")
    return config


def api_config(hashes: str, sth_api: str = None, popular=False):
    config = default_config()
    config["hashes"] = create_hash_config(hashes, popular)
    config["api"] = True
    if sth_api:
        config["api_keys"]["STH"] = sth_api
    return config


def default_config():
    defaults = {
        "api_keys": {"STH": "rGFbPbSXMF5ldzid2eyA81i6aCa497Z25MNgi8sa"},
        "hashcat": False,
        "api": False,
        "greppable": False,
        "hashes": None,
        "hashcat_binary": None,
        "timeout": 1,
        "wordlist": None,
        "offline": False,
        "hashes_dot_org": "test",
        "sth_api": "rGFbPbSXMF5ldzid2eyA81i6aCa497Z25MNgi8sa",
        "hashcat_exe_name": "hashcat",
        "hashcat_folder": "",
    }

    appname = "Search-That-Hash"
    appauthor = "HashPals"

    config_json = user_data_dir(appname, appauthor) + "\\config.json"

    if not os.path.isfile(config_json):
        os.makedirs(user_data_dir(appname, appauthor))
        with open(config_json, "w+") as file:
            file.write(json.dumps(defaults))
            file.close()

    with open(config_json) as json_file:
        json_contents = json.load(json_file)
        json_file.close()

    return json_contents


def create_hash_config(hashes, popular=False):
    # Gets the results from name-that-hash
    logging.debug("Called NTH to get hash types")
    nth_result_types = json.loads(nth.api_return_hashes_as_json(hashes, {"popular_only": popular}))
    return nth_result_types