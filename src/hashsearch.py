import hashid
import click
import sys

@click.command()
@click.option('--text', '-t')
def main(text):
    hash_identifier = hashid.HashID()
    result = hash_identifier.identifyHash(text)
    print(hashid.writeResult(result))

if __name__ == '__main__':
    main()