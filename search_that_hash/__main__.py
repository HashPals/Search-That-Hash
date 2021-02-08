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
    main()
