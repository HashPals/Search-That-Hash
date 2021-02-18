from search_that_hash.cracker.sth_mod import sth
from search_that_hash.cracker.greppable_mode_mod import runner as greppable
from search_that_hash.cracker.fast_mode_mod import runner as fast

import logging
import coloredlogs


class Handler:
    """
    This class handles the main cracking function,
    it sets the class objects and calls the correct mode
    depending on what the config is
    """

    def __init__(self, config):
        if config["api"]:
            coloredlogs.install(level=logging.CRITICAL)

        self.sth_results, self.config = sth.Sth_api.crack(config)

        self.greppable = greppable.GreppableClass(self.config, self.sth_results)
        self.fast = fast.FastClass(self.config, self.sth_results)

    def start(self):
        levels = {1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}

        if self.config["greppable"]:
            return self.greppable.greppable_crack()
        else:
            return self.fast.fast_crack()
