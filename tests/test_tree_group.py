import click
from click.testing import CliRunner
from treeclick import TreeGroup, TreeCommand


def test_custom_help():
    """Test that custom help prints without error."""
    cli = TreeGroup(name="test", help="Test CLI")

    @cli.command(name="echo", cls=TreeCommand)
    @click.argument("message")
    def echo(message):
        click.echo(message)

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output


def test_no_args_help():
    """Test that invoking without args shows help."""
    cli = TreeGroup(name="test", help="Test CLI")

    @cli.command(name="echo", cls=TreeCommand)
    @click.argument("message")
    def echo(message):
        click.echo(message)

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output
