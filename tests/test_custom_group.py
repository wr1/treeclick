import click
from click.testing import CliRunner
from treeclick import CustomGroup


def test_custom_help():
    """Test that custom help prints without error."""
    cli = CustomGroup(name="test", help="Test CLI")

    @cli.command(name="echo")
    @click.argument("message")
    def echo(message):
        click.echo(message)

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output
