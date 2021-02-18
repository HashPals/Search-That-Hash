from concurrent.futures import ThreadPoolExecutor

from search_that_hash.cracker.offline_mod import hashcat
from search_that_hash.cracker.online_mod import online

import logging
import coloredlogs


class Searcher:
    """

    This class is the one which multi threads and calls all
    the websites / API to search from

    """

    def __init__(self, config):
        logging.debug("Initing searcher")
        self.config = config
        self.searchers_offline = [hashcat.Hashcat()]
        self.searchers_online = [
            online.md5crypt(),
            online.rainbow_tabels(),
            online.nitrxgen(),
            online.cmd5(),
            online.LmRainbowTabels(),
            online.md5_addr(),
            online.md5_grom(),
            online.sha1_grom(),
            online.hashsorg(),
        ]

    def main(self, chash, types) -> dict:

        logging.info("Called main cracking function")

        return self.perform_search(self.config, chash, types)

    def perform_search(self, config, chash, types):

        config["chash"] = chash
        keys = [type["name"].lower() for type in types]
        hashcat_types = [type["hashcat"] for type in types]
        config["supported_searchers"] = []
        config["supported_types"] = []

        if not config["offline"]:
            for search in self.searchers_online:
                for hashtype in keys:
                    if "all" in search.supports:
                        config["supported_searchers"].append(search)
                        config["supported_types"].append(hashtype)
                        continue

                    if hashtype.lower() in search.supports:
                        if not search in config["supported_searchers"]:
                            config["supported_searchers"].append(search)
                        if not hashtype in types:
                            config["supported_types"].append(hashtype)

        config["supported_searchers"].append(hashcat.Hashcat())

        return self.threaded_search(config)

    def threaded_search(self, config):

        processes = []
        success = {}
        fails = {}

        with ThreadPoolExecutor(max_workers=6) as executor:
            for search in config["supported_searchers"]:
                processes.append(executor.submit(self.call_searcher, search, config))
                for (
                    possible_done
                ) in processes:  # Checks the progress of everything during cracking
                    if possible_done in success or possible_done in fails:
                        continue

                    if (
                        list(possible_done.result().values())[0] == "Failed"
                        or list(possible_done.result().values())[0] == "Not connected"
                    ):
                        fails.update(possible_done.result())
                    else:
                        success.update(possible_done.result())

                        if not self.config["greppable"]:

                            return {
                                config["chash"]: str(
                                    list(possible_done.result().values())[0]
                                )
                            }

        if success == {} and not self.config["greppable"]:
            return {config["chash"]: None}

        return {config["chash"]: [success, fails]}

    def call_searcher(self, search, future):
        try:
            return {type(search).__name__: search.crack(future)}
        except Exception as e:
            logging.warning(f"{type(search).__name__} Failed")
            return {type(search).__name__: "Failed"}
