from treeclick.custom_group import CustomGroup
from treeclick.groups.set_permissions import set_permissions

permissions = CustomGroup(name="permissions", help="Manage user permissions.")
permissions.add_command(set_permissions)
