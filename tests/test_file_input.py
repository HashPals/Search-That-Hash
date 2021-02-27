from search_that_hash import api
from click.testing import CliRunner

from search_that_hash.__main__ import main

<<<<<<< HEAD

=======
>>>>>>> ff79c8d806e2ee3906fcb5ed0ebc313fda94ce7b
def test_cli_file_no_debug():
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "tests/mocks/hashes.txt"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output

<<<<<<< HEAD

=======
>>>>>>> ff79c8d806e2ee3906fcb5ed0ebc313fda94ce7b
def test_cli_file_password_in_output():
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "tests/mocks/hashes.txt"])
    assert result.exit_code == 0
    print(result.output)
    assert "password" in result.output

<<<<<<< HEAD

=======
>>>>>>> ff79c8d806e2ee3906fcb5ed0ebc313fda94ce7b
"""def test_cli_file_password_in_b64_output():
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "tests/mocks/hashes.txt", "--base64"])
    assert result.exit_code == 0
<<<<<<< HEAD
    assert "password" not in result.output"""
=======
    assert "password" not in result.output"""
>>>>>>> ff79c8d806e2ee3906fcb5ed0ebc313fda94ce7b
