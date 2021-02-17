import json
from rich.console import Console

console = Console(highlighter=False)


class Prettifier:
    """
    This prints our output
    """

    def __init__(self, config):
        self.config = config

    @staticmethod
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

    @staticmethod
    def greppable_print(results):
        json_output = json.dumps(results, indent=4)
        print(json_output)

    @staticmethod
    def one_print(chash, result):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        console.print(
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
        )

    @staticmethod
    def error_print(msg, chash):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        console.print(
            f"\n[bold underline #E71D36]Error[/bold underline #E71D36]: [bold #E71D36]{msg}[/bold #E71D36]"
        )

    @staticmethod
    def type_print(types):
        console.print(
            f"\n[bold underline #EC7F5B]Possible Type(s)[/bold underline #EC7F5B]: [bold #AFEADC on #005F5F]{', '.join(types)}[/bold #AFEADC on #005F5F]"
        )

    @staticmethod
    def sth_print(chash, result, type, verified):
        console.print(f"\n\n[bold #011627 on #ff9f1c]{chash}[/bold #011627 on #ff9f1c]")
        texts = (
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type}[/bold #AFEADC on #005F5F]"
        )
        if not verified:
            texts += "\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this chash is this plaintext."

        console.print(texts)
