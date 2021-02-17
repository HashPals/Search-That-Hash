import json
import requests


def crack(config):
    to_del = []
    url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/lookup"
    payload = json.dumps({"Hash": list(config["hashes"].keys())})
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=config["timeout"]
        )
    except:
        return False, config

    output = response.json()["body"]
    [to_del.append(key) for key in output.keys()]

    if not config["greppable"]:
        for hash_to_del in to_del:
            del config["hashes"][hash_to_del]

    return output, config


def push(config, chash: str, result: str, types: list):
    url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/insert"
    headers = {
        "x-api-key": f"{config['api_keys']['STH']}",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"Hash": chash, "Plaintext": result, "Type": types})
    try:
        requests.request("PUT", url, headers=headers, data=payload)
    except:
        pass
