import json
import sys
import toml

import click

from search_that_hash.cracker import handler
from search_that_hash import config_object
from search_that_hash import printing

import logging
import coloredlogs


@click.command()
@click.option("--text", "-t", type=str, help="Crack a single hash.")
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=False,
    help="The file of hashes, seperated by newlines.",
)
@click.option(
    "-w",
    "--wordlist",
    type=str,
    required=False,
    help="The wordlist you want to use for Hashcat.",
)
@click.option("--timeout", type=int, help="Choose timeout in seconds.", default=3)
@click.option(
    "-g", "--greppable", is_flag=True, help="Prints as JSON, use this to grep."
)
@click.option(
    "--hashcat_binary",
    type=str,
    required=False,
    help="Location of hashcat folder (if using windows).",
)
@click.option(
    "--offline",
    "-o",
    is_flag=True,
    default=False,
    type=bool,
    help="Use offline mode. Does not search for hashes in APIs.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=int,
    help="Turn on debugging logs. -vv for max.",
)
@click.option("--accessible", is_flag=True, help="Makes the output accessible.")
@click.option("--no-banner", is_flag=True, help="Doesn't print banner.")
def main(**kwargs):
    """
    Search-That-Hash - The fastest way to crack any hash.
    \n
    GitHub:\n
            https://github.com/HashPals/Search-That-Hash\n
    Discord:\n
            https://discord.gg/CswayhQ8Ru
    \n
    Usage:
    \n
            sth --text "5f4dcc3b5aa765d61d8327deb882cf99"
    """

    if kwargs == {  # pragma: no cover
        "text": None,
        "file": None,
        "wordlist": None,
        "timeout": 3,
        "greppable": False,
        "hashcat_binary": None,
        "offline": False,
        "verbose": 0,
        "accessible": False,
        "no_banner": False,
    }:
        with click.Context(main) as ctx:
            click.echo(ctx.get_help())
            ctx.exit()

    levels = {1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}

    if kwargs["verbose"] and kwargs["verbose"] <= 3:
        coloredlogs.install(level=levels[kwargs["verbose"]])
    else:
        # Verobosity was not given so it removes logging
        coloredlogs.install(level=logging.CRITICAL)

    logging.debug("Updated logging level")
    logging.info("Called config updater")

    config = config_object.cli_config(kwargs)

    if not kwargs["greppable"] and not kwargs["accessible"] and not kwargs["no_banner"]:
        logging.info("Printing banner")
        printing.Prettifier.banner()

    cracking_handler = handler.Handler(config)
    cracking_handler.start()

    exit(0)


if __name__ == "__main__":
    main()  # pragma: no cover
