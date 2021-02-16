from search_that_hash import config_object
from search_that_hash import __main__

import json


def return_as_json(hashes):

	config = config_object.api_config(hashes)
	config["greppable"] = True

	x = __main__.cracking_handler(config)
	
	return x



def return_as_fast_json(hashes):

	config = config_object.api_config(hashes)
	
	x = __main__.cracking_handler(config)

	return x
