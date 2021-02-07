import json
import sys
import toml

import click
from loguru import logger
from name_that_hash import runner as nth
from search_that_hash.cracker import cracking

from search_that_hash import printing
from search_that_hash import config_updater
from search_that_hash import api

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
@click.option("-g", "--greppable", is_flag=True, help="Used to grep")
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
@click.option("--config", type=click.File("r"), required=False, help="File of config")
@click.option("--where", is_flag=True, help="Prints config file location")
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=int,
    help="Turn on debugging logs. -vvv for maximum logs.",
)

def main(**kwargs):

    if kwargs == {'text': None, 'file': None, 'wordlist': None, 'timeout': 1, 'hashcat': False, 'greppable': False, 'hashcat_binary': None, 'offline': False, 'config': None, 'where': False, 'verbose': 0}:
        print_help()

    if kwargs["where"]:
        print(config_updater.find_appdirs_location())
        exit(0)

    #### Logging 

    set_logger(kwargs)
    logger.debug(kwargs)

    #### Updating config from kwargs

    config = {"api":False}

    if kwargs["config"] != None:
        try:
            config["api_kys"] = toml.loads(kwargs["config"])
        except:
            config["api_keys"] = None
    else:
        # if no config is manually provided
        # check to see if one exists at appdirs
        # if it doesn't, it'll result to None
        config["api_keys"] = config_updater.read_config_file()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    config.update(kwargs)

    config["hashes"] = create_hash_config(config) # Gets hash types from NTH

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

    #### sets the logger value based on args

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

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()
    exit(0)

if __name__ == "__main__":
    main()
