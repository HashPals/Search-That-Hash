import json
import requests
from search_that_hash import printing


class Sth_api:
    def __init__(self, config, hash_processes, sth_results):
        self.hash_processes = hash_processes
        self.config = config
        self.sth_results = sth_results

    def crack(config):
        to_del = []
        url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/lookup"
        payload = json.dumps({"Hash": list(config["hashes"].keys())})
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload, timeout=config["timeout"]
            )
        except ReadTimeout:
            return (False, config)

        output = response.json()["body"]

        for key in output.keys():
            to_del.append(key)

        if not config["greppable"]:
            for hash in to_del:
                del config["hashes"][hash]

        return output, config

    def push(self, chash: str, result: str, types: list):
        url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/insert"
        headers = {
            "x-api-key": f"{self.config['api_keys']['STH']}",
            "Content-Type": "application/json",
        }
        payload = json.dumps({"Hash": chash, "Plaintext": result, "Type": types})
        try:
            requests.request("PUT", url, headers=headers, data=payload)
        except:
            pass

    def sth_output(self):
        if not self.sth_results:
            return
        for result in self.sth_results.values():
            if not self.config["api"]:
                printing.Prettifier.sth_print(
                    result["Hash"],
                    result["Plaintext"],
                    result["Type"],
                    result["Verified"],
                )
            else:
                self.results.append({result["Hash"]: result["Plaintext"]})

    def append_sth(self):
        for hash in self.hash_processes:
            base_results = list(hash.values())[0]
            try:
                base = self.sth_results[list(hash.keys())[0]]

                base_results[0].update({"STH_API": base["Plaintext"]})
                base_results.append(
                    {"Type": base["Type"], "Verified": base["Verified"]}
                )

            except KeyError:  # Not found in STH
                base_results[1].update({"STH_API": "Failed"})
                base_results.append({"Type": "Unkown", "Verified": "N/A"})

                types = []

                for type in self.config["hashes"][list(hash.keys())[0]]:
                    types.append(type["name"])
                    if len(types) == 4:
                        break  # We dont want to add all 100 possible types

                if (
                    "STH_API" not in list(base_results[0].keys())
                    and not base_results[0]
                ):
                    self.push(
                        list(hash.keys())[0],
                        list(base_results[0].values())[0],
                        types,
                    )
