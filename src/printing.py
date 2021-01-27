# Imports

import json
from typing import NamedTuple, List
from rich.console import Console
from loguru import logger

console = Console(highlighter=False)


class Prettifier:
    '''
    This prints our output
    '''

    def __init__(self, results, config):
        self.banner()
        self.pretty_print(results, config)

    def banner(self):
        banner = r"""
  _   _                          _______ _           _          _    _           _     
 | \ | |                        |__   __| |         | |        | |  | |         | |    
 |  \| | __ _ _ __ ___   ___ ______| |  | |__   __ _| |_ ______| |__| | __ _ ___| |__  
 | . ` |/ _` | '_ ` _ \ / _ \______| |  | '_ \ / _` | __|______|  __  |/ _` / __| '_ \ 
 | |\  | (_| | | | | | |  __/      | |  | | | | (_| | |_       | |  | | (_| \__ \ | | |
 |_| \_|\__,_|_| |_| |_|\___|      |_|  |_| |_|\__,_|\__|      |_|  |_|\__,_|___/_| |_|
                                                                                      
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

    def pretty_print(self, results, config):
        for new in results:
            for hash, result in new.items():
                console.print(f"\n\n[bold #011627 on #ff9f1c]{hash}[/bold #011627 on #ff9f1c]")
    
                if not result[0]:
                    console.print("\n\n[bold #2ec4b6]No results found.[/bold #2ec4b6]")
                    continue
        
                console.print(f"\n[bold underline #2ec4b6]Text[/bold underline #2ec4b6] : [bold #CCFF66]{list(result[0].values())[0]}[/bold #CCFF66]")
                console.print(f"\n[bold underline #2ec4b6]Successfull Searchers[/bold underline #2ec4b6] ✅; [bold #16c79a]{', '.join(list(result[0].keys()))}[/bold #16c79a]")
                console.print(f"\n[bold underline #2ec4b6]Successfull Searchers[/bold underline #2ec4b6] ❌; [bold #e71d36]{', '.join(list(result[1].keys()))}[/bold #e71d36]")



        console.print("\n\n")
