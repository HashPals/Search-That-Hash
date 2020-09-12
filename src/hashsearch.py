import hashid
import searcher

import click
import sys
from appdirs import *
from googlesearch import search
import toml

# import google
# from googlesearch.googlesearch import GoogleSearch
# this isnt

# The set of popular hashes
# These have priority over any other hash.
# If one hash can be MD5 or MD2, it will pick MD5 first and then MD2.
popular_hashes = set(["md5", "sha1", "sha256", "sha384", "sha512", "ntlm"])


@click.command()
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
    type=click.File("rb"),
    required=False,
    help="The file of hashes, seperated by newlines.",
)
@click.option(
    "-w", "--wordlist", type=click.File("rb"), required=False, help="The wordlist."
)
@click.option(
    "--config", type=click.File("rb"), required=False, help="File of API keys."
)
@click.option("--hashcat", is_flag=True, help="Runs Hashcat instead of John")
@click.option("--where", is_flag=True, help="Prints config file location")
def main(**kwargs):
    """HashSearch - Search Hash APIs before automatically cracking them

    """

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
        config["hashes"] = kwargs["file"].split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")

    config["hashes"] = create_hash_config(config)

    config["offline"] = kwargs["offline"]
    config["wordlist"] = kwargs["wordlist"]
    config["hashcat"] = kwargs["hashcat"]

    print(config)

    config = searcher.Searcher(config)


def create_hash_config(config):
    # Returns the hashing config
    # [{hash: {hash_types}}, {hash: {hash_types}}]
    result = []
    for hash in config["hashes"]:
        try:
            result.append({hash: get_hashid(hash)})
        except Exception as e:
            print(f"{hash} is an unknown hash type.")
            continue
    return result


def get_hashid(hash):
    hash_identifier = hashid.HashID()
    return hashid.writeResult(
        hash_identifier.identifyHash(hash)  # , None, True, True, True
    )


def read_config_file():
    return read_and_parse_config_file(find_appdirs_location())


def find_appdirs_location():
    # TODO make this OS independent the "/" makes it Windows specific
    print(user_config_dir("HashSearch", "Bee-san") + "/config.toml")
    return user_config_dir("HashSearch", "Bee-san") + "/config.toml"


def read_and_parse_config_file(file):
    config_to_parse = read_file(file)

    if config_to_parse == None:
        print("its none")
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


def hashcat():
    Pass

def John():
    Pass


def search_and_crack_hashes(config):
    """Searches hashes in APIs and then cracks the ones not found

    Args:
        list ([string]): [hashes as strings]

    Returns:
        [list]: [Plaintext of hashes]
    """
    return None


def crack_hashes(list):
    pass


if __name__ == "__main__":
    main()
