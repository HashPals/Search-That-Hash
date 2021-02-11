from search_that_hash import api
import click.testing


def test_it_works():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_json(hashes)

    assert x is not None
