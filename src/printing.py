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

    def __init__(self, des):
        self.des = des
        banner = """
   _____                     _        _______ _           _          _    _           _     
  / ____|                   | |      |__   __| |         | |        | |  | |         | |    
 | (___   ___  __ _ _ __ ___| |__ ______| |  | |__   __ _| |_ ______| |__| | __ _ ___| |__  
  \\___ \\ / _ \\/ _` | '__/ __| '_ \\______| |  | '_ \\ / _` | __|______|  __  |/ _` / __| '_ \\ 
  ____) |  __/ (_| | | | (__| | | |     | |  | | | | (_| | |_       | |  | | (_| \\__ \\ | | |
 |_____/ \\___|\\__,_|_|  \\___|_| |_|     |_|  |_| |_|\\__,_|\\__|      |_|  |_|\\__,_|___/_| |_|
                """
        
        self.test(des)


    def test(self, des):
        console.print(f"\n[bold #011627 on #ff9f1c]{des}[/bold #011627 on #ff9f1c]\n")
        console.print("[bold #2ec4b6]No hashes found.[/bold #2ec4b6]")
        console.print("\n[bold underline #2ec4b6]Least Likely[/bold underline #2ec4b6]\n")
        console.print(f"[bold #e71d36]{des}[/bold #e71d36]")
        consoleprint(f"[#ff9f1c]Summary: {des}[/#ff9f1c]")

Prettifier("hello")