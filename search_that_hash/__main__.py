import json
import sys
import toml

import click
from loguru import logger
from name_that_hash import runner as nth

from search_that_hash.cracker import cracking
from search_that_hash import config_object
from search_that_hash import printing

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


@click.command()
@click.option("--text", "-t", type=str, help="Crack a single hash")
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=False,
    help="The file of hashes, seperated by newlines.",
)
@click.option("-w", "--wordlist", type=str, required=False, help="The wordlist.")
@click.option("--timeout", type=int, help="Choose timeout time in second", default=1)
@click.option("--hashcat", is_flag=True, help="Runs Hashcat instead of John")
@click.option("--greppable", is_flag=True, help="Used to grep")
@click.option(
    "--hashcat_binary",
    type=str,
    required=False,
    help="Location of hashcat / john folder (if using windows)",
)
@click.option(
    "--offline",
    "-o",
    is_flag=True,
    default=False,
    type=bool,
    help="Use offline mode. Does not search for hashes.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=int,
    help="Turn on debugging logs. -vvv for maximum logs.",
)
def main(**kwargs):
    """
    Search That Hash - The fastest way to crack a hash.\n
    Searches Hash APIs for the answer, if not found goes straight to HashCat / John.\n

    Discord (for support):\n
        https://discord.gg/CGSDqEA
    \n
    GitHUb:\n
        https://github.com/HashPals/hashsearch \n
    A project by Bee, creator of RustScan, Ciphey, Name-That-Hash and more. Thanks to Jayyy, Fawaz, and Skeletal <3

    \n

    Usage examples:\n
        sth -t "8846F7EAEE8FB117AD06BDD830B7584C"\n
        sth -t "8846F7EAEE8FB117AD06BDD830B7584C" --offline\n
    """

    set_logger(kwargs)
    logger.debug(kwargs)

    config = {"api_keys": None, "binary": None, "api": None}

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    config.update(kwargs)
    # TODO what does this do?
    config["hashes"] = create_hash_config(config)

    if not kwargs["greppable"]:
        printing.Prettifier.banner()

    searcher = cracking.Searcher(config)
    results = cracking.Searcher.main(searcher)

    if kwargs["greppable"]:
        printing.Prettifier.grepable_print(results)

    exit(0)


def create_hash_config(config):
    # Gets the results from name-that-hash
    return json.loads(nth.api_return_hashes_as_json(config["hashes"]))


import sys

def set_logger(kwargs):
    # sets the logger value based on args
    verbosity = kwargs["verbose"]
    if not verbosity:
        logger.remove()
        return
    elif verbosity == 1:
        verbosity = "WARNING"
    elif verbosity == 2:
        verbosity = "DEBUG"
    elif verbosity == 3:
        verbosity = "TRACE"
    logger.add(sink=sys.stderr, level=verbosity, colorize=sys.stderr.isatty())
    logger.opt(colors=True)

    logger.debug(f"Verbosity set to level {verbosity} ({verbosity})")


if __name__ == "__main__":
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = (
        str(sys.version_info[0])
        + "."
        + str(sys.version_info[1])
        + "."
        + str(sys.version_info[2])
    )

    if major != 3 or (major == 3 and minor < 7):
        print(
            f"Search That Hash requires Python 3.7+, you are using {python_version}. Please install a higher Python version."
        )
        sys.exit(1)

    from search_that_hash import main

    main.main()
