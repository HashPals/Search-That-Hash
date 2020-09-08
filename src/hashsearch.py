import hashid


import click
import sys
import appdirs
from googlesearch import search
# import google
# from googlesearch.googlesearch import GoogleSearch
# this isnt 

@click.command()
@click.option('--text', '-t', type=str, help = "Crack a single hash")
@click.option("--offline", "-o", is_flag=True, default=False, type=bool, help="Use offline mode. Does not search for hashes.")
@click.option("-f", "--file", type=click.File("rb"), required=False, help="The file of hashes, seperated by newlines.")
@click.option("-w", "--wordlist", type=click.File("rb"), required=False, help="The wordlist.")
@click.option("--apiFile", type=click.File("rb"), required=False, help="File of API keys.")
@click.option("--hashcat", is_flag=True, help="Runs Hashcat instead of John")
def main(**kwargs):
    """HashSearch - Search Hash APIs before automatically cracking them

    """
    print(kwargs)
    """hash_identifier = hashid.HashID()
    result = hash_identifier.identifyHash(text)
    possible_hash_types = set(result.keys())
    print(hashid.writeResult(result))"""

def read_config_file(file):
    Pass 

def hashcat():
    Pass 

def John():
    Pass 



def search_and_crack_hashes(list):
    """Searches hashes in APIs and then cracks the ones not found

    Args:
        list ([string]): [hashes as strings]

    Returns:
        [list]: [Plaintext of hashes]
    """
    return None

def crack_hashes(list):
    pass


if __name__ == '__main__':
    main()