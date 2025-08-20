import click


@click.command(name="info")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information.")
def info(verbose):
    """Display CLI information."""
    click.echo("CLI Information")
    if verbose:
        click.echo("Detailed mode enabled.")
