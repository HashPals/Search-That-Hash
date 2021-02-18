from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker.greppable_mod import runner as greppable
from search_that_hash.cracker.fast_mod import runner as fast
import logging
import coloredlogs


class main:
    def __init__(self, config):

        if config["api"]:
            coloredlogs.install(level=logging.CRITICAL)

        self.sth_results, self.config = sth.sth_api.crack(config)

        self.greppable = greppable.main(self.config, self.sth_results)
        self.fast = fast.main(self.config, self.sth_results)

    def start(self):

        if self.config["greppable"]:
            return self.greppable.greppable_crack()
        else:
            return self.fast.fast_crack()
