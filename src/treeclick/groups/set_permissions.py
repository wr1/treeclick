import click
from treeclick.custom_group import CustomGroup


@click.command(name="add")
@click.argument("user_id", type=str)
@click.argument("permission", type=str)
def add_permission(user_id, permission):
    """Add a permission for a user."""
    click.echo(f"Adding permission {permission} for user {user_id}")


set_permissions = CustomGroup(name="set", help="Manage user permissions.")
set_permissions.add_command(add_permission)
