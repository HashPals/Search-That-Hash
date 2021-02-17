import json
import sys
import toml

import click

from search_that_hash.cracker import cracking
from search_that_hash import config_object
from search_that_hash import printing
from concurrent.futures import ThreadPoolExecutor
from search_that_hash.cracker.sth_mod import sth

import logging
import coloredlogs


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
@click.option("--timeout", type=int, help="Choose timeout time in second", default=2)
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
    help="Turn on debugging logs. -vv for max",
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

    #### LOGGING

    levels = {1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
    try:
        coloredlogs.install(level=levels[kwargs["verbose"]])
    except:
        # Verobosity was not given so it removes logging
        coloredlogs.install(level=logging.CRITICAL)

    logging.debug("Updated logging level")
    logging.info("Called config updater")

    #### UPDATING CONFIG

    config = config_object.cli_config(kwargs)

    #### BANNER

    if not kwargs["greppable"] and not kwargs["accessible"] and not kwargs["no_banner"]:
        logging.info("Printing banner")
        printing.Prettifier.banner()

    #### CALLING CRACKING

    cracking_handler(config)

    exit(0)


def cracking_handler(config):

    if config["api"]:
        coloredlogs.install(level=logging.CRITICAL)

    ### SETTING VARIBLES

    hash_processes = []
    results = []
    searcher = cracking.Searcher(config)

    #### STH CRACKING

    sth_results, config = sth.crack(config)

    if not sth_results == False:
        for result in sth_results.values():
            if not config["greppable"]:
                if not config["api"]:
                    printing.Prettifier.sth_print(
                        result["Hash"],
                        result["Plaintext"],
                        result["Type"],
                        result["Verified"],
                    )
                else:
                    results.append({result["Hash"]: result["Plaintext"]})

    #### MAIN CRACKING

    for chash, types in config["hashes"].items():
        if types == []:
            if not config["greppable"]:
                if config["api"]:
                    results.append({chash: "No types found for this hash."})
                    continue
                printing.Prettifier.error_print("No types found for this hash.", chash)
            continue

        hash_processes.append(cracking.Searcher.main(searcher, chash, types))

        #### OUTPUTTING

        chash = list(hash_processes[-1].keys())[0]
        result = hash_processes[-1][chash]

        if result == None and not config["greppable"]:
            if config["api"]:
                results.append({chash: "Could not crack hash"})
                continue
            printing.Prettifier.error_print("Could not crack hash.", chash)
            continue

        if not config["greppable"]:
            if config["api"]:
                results.append({chash: result})
                continue
            printing.Prettifier.one_print(chash, result)

    if config["greppable"]:

        #### ADDING STH RESULTS

        for hash in hash_processes:
            base_results = list(hash.values())[0]
            try:
                base = sth_results[list(hash.keys())[0]]

                base_results[0].update({"STH_API": base["Plaintext"]})
                base_results.append(
                    {"Type": base["Type"], "Verified": base["Verified"]}
                )
                """ 

				Firstly this takes the hash from the loop and gets is values

				{hash:[{COMPLETED},{FAILED}]}

				The [0] index is for the main list

				The next [0] index is for the successful dicts

				Then it updates it with STH which:

				Gets all hashes in a list and indexs the hash which its looking for

				Then it takes that plaintext and updates the successfull dict with

				{'STH_API':'Result'}
				"""

            except:
                base_results[1].update({"STH_API": "Failed"})
                base_results.append({"Type": "Unkown", "Verified": "N/A"})

                #### CHECKING IF HASH SHOULD BE PUSHED TO STH

                types = []

                for type_ in config["hashes"][list(hash.keys())[0]]:
                    types.append(type_["name"])
                    if len(types) == 4:
                        break

                if (
                    "STH_API" not in list(base_results[0].keys())
                    and base_results[0] != {}
                ):
                    sth.push(
                        config,
                        list(hash.keys())[0],
                        list(base_results[0].values())[0],
                        types,
                    )
                    # This pushes the config, hash, plaintext and types

            # This is here in case STH does not crack it, in that case it does the exact same but refers to the fail list index (0 and not 1)

        if not config["api"]:
            logging.info("Printing greppable results")
            printing.Prettifier.greppable_print(hash_processes)

        return hash_processes

    return results


if __name__ == "__main__":
    main()
