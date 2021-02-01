# Don't use Config{} here, either update the dict orr store it all in the class
class Search_that_hash_api:
    def __init__(self):
        config = {}


def return_as_json(hashes):

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = True
    config["hashes"] = hashes
    config["binary"] = False
    config["hashes"] = create_hash_config(config)
    config["api"] = Flse

    try:
        searcher = cracking.Searcher(config)
        return json.dumps(cracking.Searcher.main(searcher))
    except:
        return False


def return_as_fast_json(hashes):

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = False
    config["hashes"] = hashes
    config["binary"] = False
    config["hashes"] = create_hash_config(config)
    config["api"] = True

    try:
        searcher = cracking.Searcher(config)
        return json.dumps(cracking.Searcher.main(searcher))
    except:
        return False
