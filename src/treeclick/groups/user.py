import click
from treeclick.custom_group import CustomGroup
from treeclick.groups.manage import manage


@click.command(name="add")
@click.argument("name", type=str)
@click.option("--email", "-e", help="Email address of the user")
def add_user(name, email):
    """Add a new user to the system."""
    click.echo(f"Adding user: {name}")
    if email:
        click.echo(f"Email: {email}")


@click.command(name="list")
def list_users():
    """List all users in the system."""
    click.echo("Listing all users...")


user = CustomGroup(name="user", help="Manage user-related operations.")
user.add_command(add_user)
user.add_command(list_users)
user.add_command(manage)
