import click
from rich.console import Console
from rich.tree import Tree
from rich.text import Text

# Initialize console for rich output
console = Console()


class CustomGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.append(
            click.Option(
                ["--help"],
                is_flag=True,
                expose_value=False,
                is_eager=True,
                callback=self.print_custom_help,
            )
        )

    def print_custom_help(self, ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        console.print(
            f"\n[bold]Usage:[/bold] {ctx.command_path} [OPTIONS] COMMAND [ARGS]...\n"
        )
        console.print("[bold]Options:[/bold]")
        console.print(" --help Show this message and exit.\n")
        console.print(f"[bold]Description:[/bold] {ctx.command.help}\n")
        console.print("[bold]Commands:[/bold]")

        indent_size = 4  # Approximate indentation per level in rich tree

        # Recursive function to collect effective lengths
        def collect_effective_lengths(
            commands, level, command_effectives, option_effectives
        ):
            for cmd_name, cmd in sorted(commands.items()):
                color = "bold green" if isinstance(cmd, click.Group) else "cyan"
                args = [
                    f"[[orange1]{param.name.upper()}[/orange1]]"
                    for param in cmd.params
                    if isinstance(param, click.Argument)
                ]
                arg_str = " ".join(args) if args else ""
                left = f"[{color}]{cmd_name}[/] {arg_str}"
                left_len = console.measure(Text.from_markup(left)).maximum
                command_effectives.append(left_len + level * indent_size)
                for param in cmd.params:
                    if isinstance(param, click.Option):
                        opts = ", ".join(param.opts)
                        left = f"[bold yellow]{opts}[/bold yellow]"
                        left_len = console.measure(Text.from_markup(left)).maximum
                        option_effectives.append(left_len + (level + 1) * indent_size)
                if isinstance(cmd, click.Group) and cmd.commands:
                    collect_effective_lengths(
                        cmd.commands, level + 1, command_effectives, option_effectives
                    )

        # Collect effective lengths
        command_effectives = []
        option_effectives = []
        collect_effective_lengths(
            ctx.command.commands, 0, command_effectives, option_effectives
        )
        max_command_effective = max(command_effectives) if command_effectives else 0
        max_option_effective = max(option_effectives) if option_effectives else 0
        global_column = max(max_command_effective, max_option_effective - 4) + 1

        # Get the command path
        path = []
        current_ctx = ctx
        while current_ctx:
            path.append(current_ctx.command.name)
            current_ctx = current_ctx.parent
        path = path[::-1]  # Reverse to root first

        is_top_level = len(path) == 1

        # Recursive function to add to tree
        def add_to_tree(branch, commands, level, path, path_index):
            if level > 5:
                branch.add("[red]Recursion limit reached (max 5 levels)[/red]")
                return
            if is_top_level or path_index == len(path):
                # Show all at this level
                for cmd_name, cmd in sorted(commands.items()):
                    color = "bold green" if isinstance(cmd, click.Group) else "cyan"
                    args = [
                        f"[[orange1]{param.name.upper()}[/orange1]]"
                        for param in cmd.params
                        if isinstance(param, click.Argument)
                    ]
                    arg_str = " ".join(args) if args else ""
                    left = f"[{color}]{cmd_name}[/] {arg_str}"
                    left_text = Text.from_markup(left)
                    left_len = console.measure(left_text).maximum
                    pad = global_column - level * indent_size - left_len
                    pad_text = Text(" " * pad)
                    label = left_text + pad_text + Text(cmd.help)
                    cmd_branch = branch.add(label)
                    for param in cmd.params:
                        if isinstance(param, click.Option):
                            opts = ", ".join(param.opts)
                            left = f"[bold yellow]{opts}[/bold yellow]"
                            left_text = Text.from_markup(left)
                            left_len = console.measure(left_text).maximum
                            pad = (
                                global_column + 4 - (level + 1) * indent_size - left_len
                            )
                            pad_text = Text(" " * pad)
                            star = "[red]*[/red]" if param.required else ""
                            option_label = (
                                left_text
                                + pad_text
                                + Text(
                                    star + " " + (param.help or ""),
                                    style="italic yellow",
                                )
                            )
                            cmd_branch.add(option_label)
                    if isinstance(cmd, click.Group) and cmd.commands:
                        add_to_tree(
                            cmd_branch, cmd.commands, level + 1, path, path_index
                        )
            else:
                # Show only the path branch
                next_cmd_name = path[path_index]
                cmd = commands.get(next_cmd_name)
                if cmd:
                    color = "bold green" if isinstance(cmd, click.Group) else "cyan"
                    args = [
                        f"[[orange1]{param.name.upper()}[/orange1]]"
                        for param in cmd.params
                        if isinstance(param, click.Argument)
                    ]
                    arg_str = " ".join(args) if args else ""
                    left = f"[{color}]{next_cmd_name}[/] {arg_str}"
                    left_text = Text.from_markup(left)
                    left_len = console.measure(left_text).maximum
                    pad = global_column - level * indent_size - left_len
                    pad_text = Text(" " * pad)
                    label = left_text + pad_text + Text(cmd.help)
                    cmd_branch = branch.add(label)
                    for param in cmd.params:
                        if isinstance(param, click.Option):
                            opts = ", ".join(param.opts)
                            left = f"[bold yellow]{opts}[/bold yellow]"
                            left_text = Text.from_markup(left)
                            left_len = console.measure(left_text).maximum
                            pad = (
                                global_column + 4 - (level + 1) * indent_size - left_len
                            )
                            pad_text = Text(" " * pad)
                            star = "[red]*[/red]" if param.required else ""
                            option_label = (
                                left_text
                                + pad_text
                                + Text(
                                    star + " " + (param.help or ""),
                                    style="italic yellow",
                                )
                            )
                            cmd_branch.add(option_label)
                    if isinstance(cmd, click.Group) and cmd.commands:
                        add_to_tree(
                            cmd_branch, cmd.commands, level + 1, path, path_index + 1
                        )

        # Build the tree
        tree = Tree("", guide_style="dim")
        add_to_tree(
            tree, ctx.command.commands, 0, path, 1
        )  # Start from level 0, path_index 1 (since path[0] is cli)
        console.print(tree)
        console.print()
        ctx.exit()
