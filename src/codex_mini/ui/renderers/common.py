from rich.table import Table


def create_grid() -> Table:
    grid = Table.grid(padding=(0, 1))
    grid.add_column(no_wrap=True)
    grid.add_column(overflow="fold")
    return grid


def truncate_display(text: str, max_lines: int = 10, max_line_length: int = 1000) -> str:
    lines = text.split("\n")
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["... (more " + str(len(lines) - max_lines) + " lines)"]
    for i, line in enumerate(lines):
        if len(line) > max_line_length:
            lines[i] = (
                line[:max_line_length] + "... (more " + str(len(line) - max_line_length) + " characters in this line)"
            )
    return "\n".join(lines)
