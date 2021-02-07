import json
from search_that_hash import cracking

class Search_that_hash_api:
    def __init__(self, config):
        config = {}
        config["offline"] = False
        config["api_keys"] = False
        config["wordlist"] = False
        config["hashcat"] = False
        config["timeout"] = 1
        config["greppable"] = True
        config["binary"] = False
        config["api"] = True

    def create_hash_config(config):
        # Gets the results from name-that-hash
        return json.loads(nth.api_return_hashes_as_json(config["hashes"]))
        
    def fast(self, hashes):

        config = Search_that_hash_api.config
        config["greppable"] = False
        config["hashes"] = hashes
        config["hashes"] = Search_that_hash_api.create_hash_config(config["hashes"])

        try:
            searcher = cracking.Searcher(config)
            return json.dumps(cracking.Searcher.main(searcher))
        except:
            return False

    def info(self, hashes):

        config = Search_that_hash_api.config
        config["hashes"] = hashes
        config["hashes"] = self.create_hash_config(config["hashes"])

        try:
            searcher = cracking.Searcher(config)
            return json.dumps(cracking.Searcher.main(searcher))
        except:
            return False
search = Search_that_hash_api()
print(Search_that_hash_api.fast(search, "098f6bcd4621d373cade4e832627b4f6"))

# I cant get this to work feel free to just destory it all and rewrite it
