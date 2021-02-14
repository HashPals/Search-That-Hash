import json
import sys
import toml

import click
from loguru import logger

from search_that_hash.cracker import cracking
from search_that_hash import config_object
from search_that_hash import printing


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
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=int,
    help="Turn on debugging logs. -vvv for maximum logs.",
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
    config = config_object.cli_config(kwargs)

    if not kwargs["greppable"] and not kwargs["accessible"] and not kwargs["no_banner"]:
        printing.Prettifier.banner()

    searcher = cracking.Searcher(config)
    results = cracking.Searcher.main(searcher)

    if kwargs["greppable"]:
        printing.Prettifier.greppable_print(results)

    exit(0)

if __name__ == "__main__":
    main()