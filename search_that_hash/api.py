from search_that_hash.cracker import cracking
from search_that_hash import config_object
from search_that_hash import __main__

import json


def return_as_json(hashes):

    config = config_object.api_config(hashes)
    config["greppable"] = True

    searcher = cracking.Searcher(config)
    x = searcher.main()
    
    return x



def return_as_fast_json(hashes, sth_api):

    config = config_object.api_config(hashes, sth_api)
    searcher = cracking.Searcher(config)
    x = searcher.main()

    return x
