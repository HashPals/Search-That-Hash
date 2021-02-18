from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker import cracking
import json


class GreppableClass:
    """
    This class is in charge of handling the cracking, and formatting
    the output into JSON. It then checks for if the API is enabled
    and returns the results

    https://github.com/HashPals/Search-That-Hash/wiki/The-API-return-object
    """

    def __init__(self, config, sth_results):
        self.sth_results = sth_results
        self.config = config
        self.hash_processes = []
        self.searcher = cracking.Searcher(config)

    def greppable_crack(self):
        for chash, types in self.config["hashes"].items():
            self.hash_processes.append(
                cracking.Searcher.main(self.searcher, chash, types)
            )

        self.sth = sth.Sth_api(self.config, self.hash_processes, self.sth_results)
        self.sth.append_sth()

        if not self.config["api"]:
            print(json.dumps(self.hash_processes, indent=4))

        return self.hash_processes
