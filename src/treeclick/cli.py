from treeclick.custom_group import CustomGroup
from treeclick.commands.info import info
from treeclick.groups.project import project
from treeclick.groups.user import user

cli = CustomGroup(
    name="treeclick",
    help="This CLI provides commands to handle various tasks with subcommands for specific actions.",
)

cli.add_command(user)
cli.add_command(project)
cli.add_command(info)


def main():
    cli()


if __name__ == "__main__":
    main()
