import hashid
import click
import sys

@click.command()
@click.option('--text', '-t')
def main(text):
    hash_identifier = hashid.HashID()
    result = hash_identifier.identifyHash(text)
    possible_hash_types = set(result.keys())
    print(hashid.writeResult(result))

if __name__ == '__main__':
    main()