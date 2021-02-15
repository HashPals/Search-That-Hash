import json
from typing import List, NamedTuple

import requests
from name_that_hash import runner
from rich.console import Console

console = Console(highlighter=False)


class Prettifier:
    """
    This prints our output
    """

    def __init__(self, config):
        self.config = config

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

    def greppable_print(self, results):
        json_output = json.dumps(results, indent=4)
        print(json_output)

    def one_print(self, result, chash):
        # Fixes dictionary update sequence element #0 has length 1; 2 is required #1
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        # Handles STH API being used
        if "statusCode" in result:
            data = result["body"][chash]
            result = data["Plaintext"]
            type_hash = data["Type"]
            texts = (
                f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
                + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type_hash}[/bold #AFEADC on #005F5F]"
            )
            if not data["Verified"]:
                texts += "\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this chash is this plaintext."
            console.print(texts)
        else:
            hashes = [chash]
            output = json.loads(runner.api_return_hashes_as_json(hashes))
            types = output[chash]
            to_make = []
            for i in types:
                to_make.append(i["name"])

            self.push(chash, result, to_make)
            console.print(
                f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            )

    def sth_print(self, chash, result, type, verified):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        texts = (
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type}[/bold #AFEADC on #005F5F]"
        )
        if not verified:
            texts += "\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this chash is this plaintext."

        console.print(texts)

    def error_print(self, msg, chash):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        console.print(
            f"\n[bold underline #E71D36]Error[/bold underline #E71D36]: [bold #E71D36]{msg}[/bold #E71D36]"
        )

    def type_print(self, types):
        console.print(
            f"\n[bold underline #EC7F5B]Possible Type(s)[/bold underline #EC7F5B]: [bold #AFEADC on #005F5F]{', '.join(types)}[/bold #AFEADC on #005F5F]"
        )

    def push(self, chash: str, result: str, to_make: str):
        url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/insert"
        headers = {
            "x-api-key": f"{self.config['api_keys']['STH']}",
            "Content-Type": "application/json",
        }
        payload = json.dumps({"Hash": chash, "Plaintext": result, "Type": to_make})
        requests.request("PUT", url, headers=headers, data=payload)
