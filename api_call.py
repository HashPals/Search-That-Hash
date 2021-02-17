from search_that_hash import api

hashes = ["5f4dcc3b5aa765d61d8327deb882cf99"]

x = set(list(api.return_as_json(hashes)[0]['5f4dcc3b5aa765d61d8327deb882cf99'][0].values()))

assert 'password' in x
