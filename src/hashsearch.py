import hashid


import click
import sys
import appdirs
import google-search 

@click.command()
@click.option('--text', '-t', type=str, help = "Crack a single hash")
@click.option("--offline", "-o", is_flag=True, default=Fasle, type=bool, help="Use offline mode. Does not search for hashes.")
@click.option("-f", "--file", type=click.File("rb"), required=False, help="The file of hashes, seperated by newlines.")
@click.option("-w", "--wordlist", type=click.File("rb"), required=False, help="The wordlist.")
@click.option("--apiFile", type=click.File("rb"), required=False, help="File of API keys.")
def main(text):
    hash_identifier = hashid.HashID()
    result = hash_identifier.identifyHash(text)
    possible_hash_types = set(result.keys())
    print(hashid.writeResult(result))

def search_and_crack_hashes(list):
    """Searches hashes in APIs and then cracks the ones not found

    Args:
        list ([string]): [hashes as strings]

    Returns:
        [list]: [Plaintext of hashes]
    """
    return None

def crack_hashes(list):


if __name__ == '__main__':
    main()