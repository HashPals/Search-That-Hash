import json
from typing import NamedTuple, List
from rich.console import Console
from loguru import logger

# we need a global console to control highlighting / printing
console = Console(highlighter=False)


class Prettifier:
    """
    This classes entire existence is to output stuff.
    """

    def __init__(self, results, config):
        self.banner()
        self.pretty_print(results, config)

    def banner(self):
        banner = """
   _____                     _        _______ _           _          _    _           _     
  / ____|                   | |      |__   __| |         | |        | |  | |         | |    
 | (___   ___  __ _ _ __ ___| |__ ______| |  | |__   __ _| |_ ______| |__| | __ _ ___| |__  
  \\___ \\ / _ \\/ _` | '__/ __| '_ \\______| |  | '_ \\ / _` | __|______|  __  |/ _` / __| '_ \\ 
  ____) |  __/ (_| | | | (__| | | |     | |  | | | | (_| | |_       | |  | | (_| \\__ \\ | | |
 |_____/ \\___|\\__,_|_|  \\___|_| |_|     |_|  |_| |_|\\__,_|\\__|      |_|  |_|\\__,_|___/_| |_|
                """
        
        console.print(f"[bold blue]{banner}[/bold blue]")
        console.print(f"""[bold underline blue]
https://twitter.com/bee_sec_san
https://github.com/HashPals/Name-That-Hash
https://twitter.com/Jayy_2004 [/bold underline blue]""")

    def pretty_print(self, results, config):
        for hash, types in config["hashes"].items():
            console.print(f"\n[bold #011627 on #ff9f1c]{hash}[/bold #011627 on #ff9f1c]\n")
            console.print("\n[bold underline #2ec4b6]Results[/bold underline #2ec4b6]\n")
            for name, result in results.items():
                console.print(f"[#E71D36]{name}[/#E71D36] : {result}")
            console.print("\n[bold underline #2ec4b6]Types[/bold underline #2ec4b6]\n")
            types = [type["name"].lower() for type in types]
            for i in range(len(types)):
                console.print(f"[#E71D36]{types[i]}[/#E71D36]", end=", ")
                if i == 5:
                    break
        console.print(f"\n\n")
                
    
