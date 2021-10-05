import json
from rich.console import Console

console = Console(highlighter=False)


class Prettifier:
    """
    This prints our output
    """

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
            "https://github.com/HashPals/Search-That-Hash",
            "https://twitter.com/Jayy_2004",
        ]

        console.print(f"[bold blue]{banner}[/bold blue]")

        [
            console.print(f"[bold underline blue]{link}[/bold underline blue]")
            for link in links
        ]

    @staticmethod
    def error_print(msg, chash):
        console.print(f"\n\n[bold #ffffff on #f08400]{chash}[/bold #ffffff on #ed0010]")
        console.print(
            f"\n[bold underline #E71D36]Error[/bold underline #E71D36]: [bold #E71D36]{msg}[/bold #E71D36]"
        )

    @staticmethod
    def sth_print(chash, result, type, verified):
        console.print(f"\n\n[bold #ffffff on #ed0010]{chash}[/bold #ffffff on #ed0010]")
        texts = (
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Type[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{type}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Site[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]STH DB[/bold #AFEADC on #005F5F]"
        )
        if not verified:
            texts += "\n[bold underline #EC7F5B]Warning[/bold underline #EC7F5B]: This result is unverified. That means either our workers haven't verified it yet or it's very new. We cannot guarantee this chash is this plaintext."  # pragma: no cover

        console.print(texts)

    @staticmethod
    def one_print(chash, result, site):
        console.print(f"\n\n[bold #ffffff on #ed0010]{chash}[/bold #ffffff on #ed0010]")
        console.print(
            f"\n[bold underline #EC7F5B]Text[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]{result}[/bold #AFEADC on #005F5F]"
            + f"\n[bold underline #EC7F5B]Site[/bold underline #EC7F5B] : [bold #AFEADC on #005F5F]Hashtoolkit[/bold #AFEADC on #005F5F]"
        )
