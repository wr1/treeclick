import click.testing
from treeclick.cli import cli


def test_info():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "CLI Information" in result.output
