import json
from typing import NamedTuple, List

from rich.console import Console
from loguru import logger
import requests

from name_that_hash import runner

console = Console(highlighter=False)


class Prettifier:
    """
    This prints our output
    """

    def __init__(self, results, config):
        self.banner()

    def banner():
        banner = r"""
  _____                     _        _______ _           _          _    _           _     
 / ____|                   | |      |__   __| |         | |        | |  | |         | |    
| (___   ___  __ _ _ __ ___| |__ ______| |  | |__   __ _| |_ ______| |__| | __ _ ___| |__  
 \___ \ / _ \/ _` | '__/ __| '_ \______| |  | '_ \ / _` | __|______|  __  |/ _` / __| '_ \ 
 ____) |  __/ (_| | | | (__| | | |     | |  | | | | (_| | |_       | |  | | (_| \__ \ | | |
|_____/ \___|\__,_|_|  \___|_| |_|     |_|  |_| |_|\__,_|\__|      |_|  |_|\__,_|___/_| |_|                                                                                           																		  
		"""

        links = [
            "https://twitter.com/bee_sec_san",
            "https://github.com/HashPals/Name-That-Hash",
            "https://twitter.com/Jayy_2004",
        ]

        console.print(f"[bold blue]{banner}[/bold blue]")

        [
            console.print(f"[bold underline blue]{link}[/bold underline blue]")
            for link in links
        ]

    def grepable_print(results):
        JSON = json.dumps(results, indent=4)
        print(JSON)

    def one_print(result, hash):
        # Fixes dictionary update sequence element #0 has length 1; 2 is required #1
        console.print(f"\n\n[bold #011627 on #ff9f1c]{hash}[/bold #011627 on #ff9f1c]")
        if "statusCode" in result: # Handles STH API being given
            data = result["body"][hash]
            result = data["Plaintext"]
            type_hash = data["Type"]
            texts = (
                f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
                + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type_hash}[/bold #AFEADC on #005F5F]"
            )
            if not data["Verified"]:
                texts += f"\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this hash is this plaintext."
            console.print(texts)
        else:
            hashes = [hash]
            output = json.loads(runner.api_return_hashes_as_json(hashes))
            types = output[hash]
            to_make = []
            for i in types:
                to_make.append(i["name"])

            url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/insert"
            headers = {
            'x-api-key': 'rGFbPbSXMF5ldzid2eyA81i6aCa497Z25MNgi8sa',
            'Content-Type': 'application/json'
            }
            payload = {"Hash": hash, "Plaintext": result, "Type": to_make}
            response = requests.request("PUT", url, headers=headers, data=payload)
            console.print(
                f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            )

    def sth_print(hash, result, type, verified):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{hash}[/bold #011627 on #ff9f1c]")
        texts = (
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type}[/bold #AFEADC on #005F5F]"
            )
        if not verified:
            texts += f"\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this hash is this plaintext."
    
        console.print(texts)
