import re
import sys
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
    result = runner.invoke(cli, ["--help"], color=True, prog_name="test")
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
    result = runner.invoke(cli, [], color=True, prog_name="test")
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output


def test_subcommand_help_formatting():
    """Test help formatting for subcommand, including dimming and line wrapping."""
    cli = TreeGroup(
        name="test",
        help="This is a test CLI with a long description that should wrap properly in the output.",
    )

    subgroup = TreeGroup(
        name="sub", help="Subgroup with long help text that needs wrapping."
    )
    cli.add_command(subgroup)

    @subgroup.command(name="cmd", cls=TreeCommand)
    @click.option(
        "--opt",
        "-o",
        help="Option with very long help text that should wrap correctly and not dim since it's current.",
    )
    def cmd(opt):
        pass

    runner = CliRunner()
    original_argv = sys.argv
    sys.argv = ["test"]
    try:
        result = runner.invoke(
            cli, ["sub", "cmd", "--help"], color=True, prog_name="test"
        )
    finally:
        sys.argv = original_argv
    assert result.exit_code == 0
    output = re.sub(
        r"\x1b\[[0-9;]*m", "", result.output
    )  # Strip ANSI codes for assertion
    assert "Usage: test sub cmd [OPTIONS]" in output
    assert "Description: " in output
    assert "Options:" in output
    assert "--opt, -o" in output
    assert "Commands:" in output
    assert "test" in output  # Root
    assert "sub" in output  # Subgroup
    assert "cmd" in output  # Command

    # Check for dimming (though hard to assert directly, ensure structure)
    assert "This is a test CLI with a long description" in output
    assert "Option with very long help text" in output


def test_line_wrapping_in_help():
    """Test line wrapping in help text."""
    cli = TreeGroup(
        name="test",
        help="Long help text that should wrap across multiple lines without failing indentation.",
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"], color=True, prog_name="test")
    assert result.exit_code == 0
    output = result.output
    assert "Long help text that should wrap" in output
    # Ensure no failed wrapping (e.g., check for unexpected line breaks)
    assert re.search(r"wrap\s+across", output) is not None


def test_options_in_tree():
    """Test that options are included in the tree view for the current command."""
    cli = TreeGroup(name="test", help="Test CLI")

    @cli.command(name="cmd", cls=TreeCommand)
    @click.option("--opt", help="Test option")
    def cmd(opt):
        pass

    runner = CliRunner()
    result = runner.invoke(cli, ["cmd", "--help"], color=True, prog_name="test")
    assert result.exit_code == 0
    output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "--opt" in output
    assert "Test option" in output


def test_dimming_higher_levels():
    """Test dimming of higher hierarchical levels."""
    cli = TreeGroup(name="test", help="Root help")

    subgroup = TreeGroup(name="sub", help="Sub help")
    cli.add_command(subgroup)

    @subgroup.command(name="cmd", cls=TreeCommand)
    def cmd():
        pass

    runner = CliRunner()
    original_argv = sys.argv
    sys.argv = ["test"]
    try:
        result = runner.invoke(
            cli, ["sub", "cmd", "--help"], color=True, prog_name="test"
        )
    finally:
        sys.argv = original_argv
    assert result.exit_code == 0
    # Since dimming uses ANSI, check for presence of dim style codes
    assert "\x1b[2m" in result.output  # Dim style code


def test_indented_mode():
    """Test indented mode without tree visualization."""
    cli = TreeGroup(name="test", help="Test CLI", use_tree=False)

    @cli.command(name="echo", cls=TreeCommand)
    @click.argument("message")
    def echo(message):
        click.echo(message)

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"], color=True, prog_name="test")
    assert result.exit_code == 0
    assert "\u2500" not in result.output  # Guides concealed
    assert "echo" in result.output


def test_custom_max_width():
    """Test custom max_width for wrapping."""
    cli = TreeGroup(
        name="test",
        help="Very long help text that should wrap at custom width.",
        max_width=50,
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"], color=True, prog_name="test")
    assert result.exit_code == 0
    output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    # Check if wrapped within 50 chars
    help_lines = [
        line
        for line in output.split("\n")
        if "Very long help text" in line or "should wrap at custom width" in line
    ]
    for line in help_lines:
        assert len(line.strip()) <= 50


def test_config_propagation():
    """Test configuration propagation to subgroups."""
    cli = TreeGroup(name="test", help="Root", use_tree=False, max_width=60)

    subgroup = TreeGroup(name="sub", help="Sub")
    cli.add_command(subgroup)

    @subgroup.command(name="cmd", cls=TreeCommand)
    def cmd():
        pass

    # Check if config propagated
    assert not subgroup.use_tree
    assert subgroup.max_width == 60

    runner = CliRunner()
    result = runner.invoke(cli, ["sub", "--help"], color=True, prog_name="test")
    assert result.exit_code == 0
    output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "Usage: test sub [OPTIONS] COMMAND [ARGS]..." in output
