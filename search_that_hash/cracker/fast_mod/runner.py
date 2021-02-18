from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker import cracking
from search_that_hash import printing


class main:
    def __init__(self, config, sth_results):
        self.config = config
        self.hash_processes = []
        self.searcher = cracking.Searcher(config)
        self.sth = sth.sth_api(self.config, self.hash_processes, sth_results)

    def fast_crack(self):

        self.sth.sth_output()

        for chash, types in self.config["hashes"].items():

            self.hash_processes.append(
                cracking.Searcher.main(self.searcher, chash, types)
            )

            if types == []:
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
