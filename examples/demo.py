import click
from treeclick import TreeGroup, TreeCommand


# Define the CLI as TreeGroup with configuration
cli = TreeGroup(
    name="demo",
    help="This CLI provides commands to handle various tasks with subcommands for specific actions.",
    use_tree=True,
    max_width=120,
)

# First subgroup (config propagated automatically)
user = TreeGroup(name="user", help="Manage user-related operations.")
cli.add_command(user)

# Sub-subgroup under user
manage = TreeGroup(name="manage", help="Manage user settings and permissions.")
user.add_command(manage)


# Subcommand under manage (third layer)
@click.command(name="set-role", cls=TreeCommand)
@click.argument("role", type=str)
@click.option(
    "--user-id",
    "-u",
    help="User ID to set role for (unspecified if not provided) massively long yhammering on and on and on and one",
)
def set_role(role, user_id):
    """Set a role for a user."""
    click.echo(f"Setting role {role} for user ID {user_id or 'unspecified'}")


manage.add_command(set_role)


# Subcommand under manage (third layer)
@click.command(name="remove-role", cls=TreeCommand)
@click.argument("role", type=str)
@click.argument("user_id", type=str)
def remove_role(role, user_id):
    """Remove a role from a user."""
    click.echo(f"Removing role {role} for user {user_id}")


manage.add_command(remove_role)


# Subcommand for user group
@click.command(name="add", cls=TreeCommand)
@click.argument("name", type=str)
@click.option("--email", "-e", help="Email address of the user")
def add_user(name, email):
    """Add a new user to the system."""
    click.echo(f"Adding user: {name}")
    if email:
        click.echo(f"Email: {email}")


user.add_command(add_user)


# Subcommand for user group
@click.command(name="list", cls=TreeCommand)
def list_users():
    """List all users in the system."""
    click.echo("Listing all users...")


user.add_command(list_users)

# Second subgroup (no subcommands to test robustness)
project = TreeGroup(name="project", help="Manage project-related operations.")
cli.add_command(project)


# Standalone command (to test robustness)
@click.command(name="info", cls=TreeCommand)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information.")
def info(verbose):
    """Display CLI information."""
    click.echo("CLI Information")
    if verbose:
        click.echo("Detailed mode enabled.")


cli.add_command(info)

# Define permissions group under manage
permissions = TreeGroup(name="permissions", help="Manage user permissions.")
manage.add_command(permissions)

# Define set group under permissions
set_permissions = TreeGroup(name="set", help="Manage user permissions.")
permissions.add_command(set_permissions)


# Add command under set
@click.command(name="add", cls=TreeCommand)
@click.argument("user_id", type=str)
@click.argument("permission", type=str)
def add_permission(user_id, permission):
    """Add a permission for a user."""
    click.echo(f"Adding permission {permission} for user {user_id}")


set_permissions.add_command(add_permission)

if __name__ == "__main__":
    cli()
