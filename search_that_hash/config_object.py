import toml
from appdirs import *
from name_that_hash import runner as nth
import json


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
    config = defult_config()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    config["hashes"] = create_hash_config(config["hashes"])

    config.update(kwargs)

    return config

def api_config(hashes):
    config = defult_config()
    config["hashes"] = create_hash_config(hashes)
    config["api"] = True
    return config

def defult_config():
    return({"api_keys": None, "hashcat": False, "api": False, "greppable": False, "hashes":None, "hashcat_binary":None, "timeout":1, "wordlist":None, "offline":False })

def create_hash_config(hashes):
    # Gets the results from name-that-hash
    return json.loads(nth.api_return_hashes_as_json(hashes))