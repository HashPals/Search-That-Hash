from search_that_hash import config_object
from search_that_hash import __main__
from search_that_hash.cracker import handler
import json


def return_as_json(hashes):

    config = config_object.api_config(hashes)
    config["greppable"] = True
    cracking_handler = handler.main(config)

    x = cracking_handler.start()

    return x


def return_as_fast_json(hashes):

    config = config_object.api_config(hashes)
    cracking_handler = handler.main(config)

    x = cracking_handler.start()

    return x
