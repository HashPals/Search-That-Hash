from search_that_hash import api
from click.testing import CliRunner
from appdirs import *
from search_that_hash.__main__ import main
import os.path


def test_it_works():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_json(hashes)

    assert x is not None

def test_api_popular():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_json(hashes, popular=True)

    assert x is not None


def test_it_works_fast():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_fast_json(hashes)

    assert x is not None

def test_it_works_fast_popular():

    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_fast_json(hashes, popular=True)

    assert x is not None

def test_password_in_md5():

    hashes = ["5f4dcc3b5aa765d61d8327deb882cf99"]

    x = set(
        list(
            api.return_as_json(hashes)[0]["5f4dcc3b5aa765d61d8327deb882cf99"][
                0
            ].values()
        )
    )

    assert "password" in x


def test_password_in_sha512():

    hashes = [
        "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
    ]

    x = set(
        list(
            api.return_as_json(hashes)[0][
                "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
            ][0].values()
        )
    )

    assert "password" in x


def test_if_site_cli():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "\nSite : STH DB\n" in result.output


def test_cli_config_works():
    from search_that_hash import config_object

    assert "api_key" in str(
        config_object.cli_config(
            {"text": "98B243DC240F6D21AAD3B435B51404EE", "file": None}
        )
    )


def test_one_print():
    from search_that_hash import printing

    printing.Prettifier.one_print("Test", "Test", "Test")


def test_help_menu_shows_on_no_input():
    runner = CliRunner()
    result = runner.invoke(main)
    assert "Search-That-Hash - The fastest way to crack any hash." in result.output


def test_gives_timeout_and_other_args_but_not_hash():
    runner = CliRunner()
    result = runner.invoke(main, ["-vvv", "--timeout", 1])
    assert result.exit_code == 0
    assert "Error" in result.output


def test_cli():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "password" in result.output


def test_cli_no_debug():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output


def test_cli_hash_type():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "-t",
            "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
        ],
    )
    assert result.exit_code == 0
    assert "password" in result.output
    assert "SHA-512" in result.output


def test_cli_greppable_no_text():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99", "-g"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output
    assert "_____" not in result.output
    assert "https://twitter.com/bee_sec_san" not in result.output


def test_cli_verbose():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99", "-vv"])
    assert result.exit_code == 0
    assert "INFO" in result.output


def test_cli_output():
    runner = CliRunner()
    result = runner.invoke(main, ["-t", "5f4dcc3b5aa765d61d8327deb882cf99"])
    assert result.exit_code == 0
    assert "password\nType" in result.output
    assert "MD5\n" in result.output


def test_sth_api_key():
    hashes = ["5d41402abc4b2a76b9719d911017c592"]

    x = api.return_as_fast_json(hashes, "meow")

    assert x is not None


def test_cli_fail_on_grep():  # Fixes #63 issue
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["-t", "jadjsjhd9239uh80dahjdah8isdh90wq90hj0j9fj9023j0-12j-j-0fasj0a", "-g"],
    )
    assert result.exit_code == 0


def test_config_is_there():
    appname = "Search-That-Hash"
    appauthor = "HashPals"

    config_json = user_data_dir(appname, appauthor) + "\\config.json"

    assert os.path.isfile(config_json) == True