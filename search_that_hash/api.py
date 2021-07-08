from search_that_hash import config_object
from search_that_hash import __main__
from search_that_hash.cracker import handler
import json


def return_as_json(hashes, api_key=None, popular=False):

    config = config_object.api_config(hashes, api_key, popular)
    config["greppable"] = True
    cracking_handler = handler.Handler(config)

    json_result = cracking_handler.start()

    return json_result


def return_as_fast_json(hashes, api_key=None, popular=False):

    config = config_object.api_config(hashes, api_key, popular)
    cracking_handler = handler.Handler(config)

    json_result = cracking_handler.start()

    return json_result