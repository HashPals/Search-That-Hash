from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

from loguru import logger as logger

from search_that_hash import printing

from search_that_hash.cracker.offline_mod import hashcat
from search_that_hash.cracker.online_mod import online

import logging
import coloredlogs

class Searcher:
    def __init__(self, config):
        logger.trace("Initing searcher")
        logger.debug("help")
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
        self.prettifier_obj = printing.Prettifier(self.config)
        self.Hash_input = namedtuple("Hash_input", ["text", "types", "hashcat_types"])
    
    def main(self):

        logging.info("Called main cracking function")

        return self.perform_search(self.config)

    def perform_search(self, config):

        out = []
        sth_found_hashes = []

        if not config["offline"]:
            try:
                results = online.sth_api.crack(list(config["hashes"].keys()))

                for chash, values in results["body"].items():
                    sth_found_hashes.append(chash)
                    if not config["greppable"]:
                        if config["api"]:
                            out.append({chash: values["Plaintext"]})
                        else:
                            self.prettifier_obj.sth_print(
                                chash,
                                values["Plaintext"],
                                values["Type"],
                                values["Verified"],
                            )
                for hash_to_remove in sth_found_hashes:
                    del config["hashes"][hash_to_remove]
            except:
                logging.warning("STH Failed")
                pass

        if not config["timeout"]:
            logging.info("Timeout set to 1")
            config["timeout"] = 1

        for chash, types in config["hashes"].items():
            hash_ctext = chash

            keys = [type["name"].lower() for type in types]
            hashcat_types = [type["hashcat"] for type in types]
            supported_searchers = []
            types = []

            if keys == [] and not config["greppable"]:
                self.prettifier_obj.error_print(
                    "Could not find any types for this chash", hash_ctext
                )
                return

            if not config["offline"]:
                for search in self.searchers_online:
                    for hashtype in keys:
                        if "all" in search.supports:
                            supported_searchers.append(search)
                            types.append(hashtype)
                            continue

                        if hashtype.lower() in search.supports:
                            if not search in supported_searchers:
                                supported_searchers.append(search)
                            if not hashtype in types:
                                types.append(hashtype)

            supported_searchers.append(hashcat.Hashcat())

            future = self.Hash_input(hash_ctext, types, hashcat_types)

            out.append(self.threaded_search(future, supported_searchers))

        return out

    def threaded_search(self, future, supported_searchers):

        processes = []
        success = {}
        fails = {}

        with ThreadPoolExecutor(max_workers=6) as executor:
            for search in supported_searchers:
                processes.append(executor.submit(self.call_searcher, search, future))
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

                        if not self.config[
                            "greppable"  # Checks if greppable, if not then skips goes fast, if yes then returns and prints JSON.
                        ]:  # Prints without waiting for other threads to finish.

                            if not self.config["api"]:
                                self.prettifier_obj.one_print(
                                    list(possible_done.result().values())[0],
                                    future[0],
                                )
                                return
                            return {
                                future[0]: str(list(possible_done.result().values())[0])
                            }

        if success == {} and not self.config["greppable"]:
            self.prettifier_obj.error_print("Could not find plaintext", future[0])
            self.prettifier_obj.type_print(future[1])

        return {future[0]: [success, fails]}

    def call_searcher(self, search, future):
        try:
            return {type(search).__name__: search.crack(future)}
        except Exception as e:
            logging.warning(f"{type(search).__name__} Failed")
            return {type(search).__name__: "Failed"}
