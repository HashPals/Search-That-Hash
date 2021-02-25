from search_that_hash import api
from click.testing import CliRunner

from search_that_hash.__main__ import main

def test_cli_no_debug():
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "tests/mocks/hashes.txt"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output