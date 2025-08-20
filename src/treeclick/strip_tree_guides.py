def strip_tree_guides(text):
    """Replace tree guides with spaces."""
    space_connector = " " * 4
    lines = text.splitlines()
    for i in range(len(lines)):
        line = lines[i]
        line = line.replace("├── ", space_connector)
        line = line.replace("└── ", space_connector)
        line = line.replace("│   ", space_connector)
        lines[i] = line
    return "\n".join(lines) + "\n"
