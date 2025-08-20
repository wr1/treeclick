import click
from treeclick.custom_group import CustomGroup
from treeclick.groups.permissions import permissions


@click.command(name="set-role")
@click.argument("role", type=str)
@click.option(
    "--user-id",
    "-u",
    help="User ID to set role for (unspecified if not provided) massively long yhammering on and on and on and one",
)
def set_role(role, user_id):
    """Set a role for a user."""
    click.echo(f"Setting role {role} for user ID {user_id or 'unspecified'}")


@click.command(name="remove-role")
@click.argument("role", type=str)
@click.argument("user_id", type=str)
def remove_role(role, user_id):
    """Remove a role from a user."""
    click.echo(f"Removing role {role} for user {user_id}")


manage = CustomGroup(name="manage", help="Manage user settings and permissions.")
manage.add_command(set_role)
manage.add_command(remove_role)
manage.add_command(permissions)
