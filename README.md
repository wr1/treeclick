# TreeClick

A Click extension that provides tree-formatted help messages for CLI commands and groups. Inspired by [rich-click](https://github.com/ewels/rich-click).

## Installation

You can install TreeClick using pip:

```bash
pip install treeclick
```

## Usage

Import `TreeGroup` and `TreeCommand` from `treeclick` and use them instead of Click's `Group` and `Command`.

### Example

```python
import click
from treeclick import TreeGroup, TreeCommand

cli = TreeGroup(name="mycli", help="My CLI tool.")

@cli.command(name="hello", cls=TreeCommand)
@click.argument("name")
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

Running `python mycli.py --help` will display a tree-formatted help message.

For a more complex example, see `examples/demo.py`.

## Features

- Tree-structured help output using Rich.
- Automatic handling of subcommands and options.
- Dimmed higher-level hierarchy in help for subcommands.
- Consistent formatting across levels.

## License

MIT

