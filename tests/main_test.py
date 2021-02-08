from search_that_hash import main
import click.testing


def test_it_works():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = main.return_as_json(hashes)

    assert x is not None


def test_it_cracks_correctly():
    hashes = ["098f6bcd4621d373cade4e832627b4f6"]

    x = main.return_as_json(hashes)

    assert "test" in x


def test_main_succeeds():
    runn = click.testing.CliRunner()
    result = runn.invoke(main.main)

    assert result.exit_code == 0
