from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker import cracking
import json


class main:
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

        self.sth = sth.sth_api(self.config, self.hash_processes, self.sth_results)
        self.sth.append_sth()

        if not self.config["api"]:
            print(json.dumps(self.hash_processes, indent=4))

        return self.hash_processes
