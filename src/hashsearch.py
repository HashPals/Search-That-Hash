import json
from name_that_hash import runner

import click
import sys
from appdirs import *

import toml
import cracking
from printing import Prettifier

# import google
# from googlesearch.googlesearch import GoogleSearch
# this isnt

# The set of popular hashes
# These have priority over any other hash.
# If one hash can be MD5 or MD2, it will pick MD5 first and then MD2.


@click.command()
@click.option("--timeout", type=int, help="Choose timeout time in second")
@click.option("--text", "-t", type=str, help="Crack a single hash")
@click.option(
    "--offline",
    "-o",
    is_flag=True,
    default=False,
    type=bool,
    help="Use offline mode. Does not search for hashes.",
)
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=False,
    help="The file of hashes, seperated by newlines.",
)
@click.option(
    "-w", "--wordlist", type=click.File("r"), required=False, help="The wordlist."
)
@click.option(
    "--config", type=click.File("r"), required=False, help="File of API keys."
)
@click.option("--hashcat", is_flag=True, help="Runs Hashcat instead of John")
@click.option("--where", is_flag=True, help="Prints config file location")
@click.option("--greppable", is_flag=True, help="Used to grep")


# MAIN FUNCTION VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV


def main(**kwargs):

    if kwargs["where"] == True:
        print(find_appdirs_location())
        exit(0)

    config = {}

    if kwargs["config"] != None:
        try:
            config["api_keys"] = toml.loads(kwargs["config"])
        except:
            config["api_keys"] = None
    else:
        # if no config is manually provided
        # check to see if one exists at appdirs
        # if it doesn't, it'll result to None
        config["api_keys"] = read_config_file()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")

    config["hashes"] = create_hash_config(config)

    config["offline"] = kwargs["offline"]
    config["wordlist"] = kwargs["wordlist"]
    config["hashcat"] = kwargs["hashcat"]
    config["timeout"] = kwargs["timeout"]
    config["greppable"] = kwargs["greppable"]

    Prettifier.banner()

    searcher = cracking.Searcher(config)
    cracking.Searcher.main(searcher)

    # printing.Prettifier(results, config)


def return_as_json(hashes):

    config = {}

    config["hashes"] = hashes
    config["offline"] = False
    config["timeout"] = 1
    config["greppable"] = True

    searcher = cracking.Searcher(config)

    return cracking.Searcher.main(searcher)


def create_hash_config(config):
    try:
        return json.loads(runner.api_return_hashes_as_json(config["hashes"]))
    except:
        print("Invalid hash type")
        exit(0)


# CONFIG FILE FUNCTIONS VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV


def read_config_file():
    return read_and_parse_config_file(find_appdirs_location())


def find_appdirs_location():
    # TODO make this OS independent the "/" makes it Windows specific
    # print(user_config_dir("HashSearch", "Bee-san") + "/config.toml")
    return user_config_dir("HashSearch", "Bee-san") + "/config.toml"


def read_and_parse_config_file(file):
    config_to_parse = read_file(file)

    if config_to_parse == None:
        # print("its none")
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
    
if __name__ == "__main__":
    main()
