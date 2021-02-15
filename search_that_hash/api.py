from search_that_hash.cracker import cracking
from search_that_hash import config_object
from search_that_hash import __main__

import json


def return_as_json(hashes):

    config = config_object.api_config(hashes)
    config["greppable"] = True

    try:
        searcher = cracking.Searcher(config)
        return json.dumps(cracking.Searcher.main(searcher))
    except:
        return False


def return_as_fast_json(hashes):

    config = config_object.api_config(hashes)
    searcher = cracking.Searcher(config)

    return json.dumps(cracking.Searcher.main(searcher))
