from search_that_hash.cracker import cracking
from search_that_hash import __main__

import json

print("Is this file being ran")

def return_as_json(hashes):

    print("Is return as JSON being called")

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = True
    config["hashes"] = hashes
    config["hashcat_binary"] = False
    config["hashes"] = __main__.create_hash_config(config)
    config["api"] = True

    try:
        searcher = cracking.Searcher(config)
        return json.dumps(cracking.Searcher.main(searcher))
    except:
        return False


def return_as_fast_json(hashes):
    print("IS return as fast being called")

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = False
    config["hashes"] = hashes
    config["hashcat_binary"] = False
    config["hashes"] = __main__.create_hash_config(config)
    config["api"] = True

    searcher = cracking.Searcher(config)
    return json.dumps(cracking.Searcher.main(searcher))

