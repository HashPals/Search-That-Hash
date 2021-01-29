# Debugging

from loguru import logger

# Other

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

# Files

from printing import Prettifier
import online
import offline


class Searcher:
    def __init__(self, config):
        # logger.debug("called class searcher")
        self.config = config
        self.searchers_offline = [offline.hashcat()]
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
        self.Hash_input = namedtuple(
            "Hash_input",
            ["text", "types", "hashcats", "api_keys", "timeout", "greppable"],
        )

    def main(self):

        # logger.debug("called main self")
        return self.perform_search(self.config)

    def perform_search(self, config):

        out = []

        if not config["timeout"]:
            # logger.debug("Defulting timeout to 1")
            config["timeout"] = 1

        # print(config["timeout"])

        for hash, types in config["hashes"].items():
            hash_ctext = hash

            keys = [type["name"].lower() for type in types]
            hashcats = [type["hashcat"] for type in types]

            # logger.debug(f"Possible types are {keys}")

            # logger.debug(f"Called hash cracker {hash_ctext}")

            supported_searchers = []
            types = []

            if not config["offline"]:
                for search in self.searchers_online:
                    for hashtype in keys:
                        if hashtype.lower() in search.supports:
                            if not search in supported_searchers:
                                supported_searchers.append(search)
                            if not hashtype in types:
                                types.append(hashtype)

            for search in self.searchers_offline:
                for hashtype in keys:
                    if hashtype.lower() in search.supports:
                        supported_searchers.append(search)
                        if not hashtype in types:
                            iypes.append(hashtype)

            # logger.debug(f"Supported searchers are {supported_searchers}")
            # logger.debug(f"Supported Types are {types}")

            future = self.Hash_input(
                hash_ctext,
                types,
                hashcats,
                config["api_keys"],
                config["timeout"],
                config["greppable"],
            )

            # logger.debug(f"Future is {future}")

            out.append(self.threaded_search(future, supported_searchers))

            # logger.debug(f"Result is {out[-1]}")

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
                ) in (
                    processes
                ):  ## Okay so this basically checks the progress of everything during cracking :P
                    if possible_done in success or possible_done in fails:
                        continue

                    if (
                        list(possible_done.result().values())[0] == "Failed"
                        or list(possible_done.result().values())[0] == "Not connected"
                    ):
                        fails.update(possible_done.result())
                    else:
                        success.update(possible_done.result())

                        if not future[
                            5
                        ]:  # Just prints it without waiting for everything to finish
                            Prettifier.one_print(
                                str(list(possible_done.result().values())[0]), future[0]
                            )
                            return {
                                future[0]: str(list(possible_done.result().values())[0])
                            }

            if not future[5]:
                Prettifier.one_print("Not Found", future[0])
                return {future[0]: "Failed"}

        # logger.debug("Returned, ", {future[0] : [success, fails]})
        return {future[0]: [success, fadils]}

    def call_searcher(self, search, future):
        try:
            # logger.debug(f"Called {type(search).__name__}")
            return {type(search).__name__: search.crack(future)}
        except Exception as e:
            # logger.debug(f"{type(search).__name__} [{e}]")
            return {type(search).__name__: "Failed"}
