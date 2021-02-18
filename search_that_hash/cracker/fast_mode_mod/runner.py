from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker import cracking
from search_that_hash import printing


class FastClass:
    """
    This class handles the cracking and prints the results as it goes a long,
    it also checks for if the API is enabled and returns it

    https://github.com/HashPals/Search-That-Hash/wiki/The-API-return-object
    """

    def __init__(self, config, sth_results):
        self.config = config
        self.hash_processes = []
        self.searcher = cracking.Searcher(config)
        self.sth = sth.Sth_api(self.config, self.hash_processes, sth_results)
        self.results = []

    def fast_crack(self):

        results = self.sth.sth_output()
        self.results.extend(results)

        for chash, types in self.config["hashes"].items():

            self.hash_processes.append(
                cracking.Searcher.main(self.searcher, chash, types)
            )

            if not types:
                if self.config["api"]:
                    self.results.append({chash: "No types found for this hash."})
                    continue
                printing.Prettifier.error_print("No types found for this hash.", chash)
                continue

            chash: str = list(self.hash_processes[-1].keys())[0]
            result: str = self.hash_processes[-1][chash]

            if not result:
                if self.config["api"]:
                    self.results.append({chash: "Could not crack hash"})
                    continue
                printing.Prettifier.error_print("Could not crack hash.", chash)
                continue

            if self.config["api"]:
                self.results.append({chash: result})
                continue

            printing.Prettifier.one_print(chash, result)

        return self.results
