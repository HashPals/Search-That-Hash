import json
from typing import NamedTuple, List

from rich.console import Console
from loguru import logger

console = Console(highlighter=False)


class Prettifier:
    """
    This prints our output
    """

    def __init__(self, results, config):
        self.banner()
        self.pretty_print(results, config)

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
        console.print(f"\n\n[bold #011627 on #ff9f1c]{hash}[/bold #011627 on #ff9f1c]")
        console.print(
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
        )
