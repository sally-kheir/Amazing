from typing import Any, Set, Tuple, Dict, List
from typing import Optional, TypedDict, Union, cast


COLORS: Dict[str, Union[str, List[str]]] = {
    "RESET": "\033[0m",

    "ENTRY": "\033[48;2;204;224;146m",
    "EXIT": "\033[48;2;204;224;146m",

    "PALETTE_WALL": "\033[48;2;186;176;149m",
    "PALETTE_PATH": "\033[48;2;204;224;146m",
    "PALETTE_BG": "\033[48;2;237;232;208m",
    "PALETTE_PATTERN": "\033[48;2;214;211;154m",

    "MAGENTA_WALL": "\033[48;2;103;0;103m",
    "MAGENTA_BG": "\033[48;2;255;173;255m",
    "MAGENTA_PATH": "\033[48;2;167;69;214m",
    "MAGENTA_PATTERN": "\033[48;2;193;28;132m",

    "PASTEL_WALL": "\033[48;2;216;164;181m",
    "PASTEL_BG": "\033[48;2;242;231;189m",
    "PASTEL_PATH": "\033[48;2;189;217;242m",
    "PASTEL_PATTERN": "\033[48;2;242;189;205m",
    "PASTEL_START_END": "\033[48;2;189;217;242m",

    "NEON_WALL": "\033[48;2;184;92;207m",
    "NEON_BG": "\033[48;2;255;179;243m",
    "NEON_PATH": "\033[48;2;115;255;223m",
    "NEON_PATTERN": "\033[48;2;223;115;255m",
    "NEON_START": "\033[48;2;255;115;215m",
    "NEON_EXIT": "\033[48;2;175;255;237m",
}


class ThemeStyle(TypedDict):
    """Full style associated with a theme."""

    wall: str
    path: str
    pattern: str
    pattern_display: str


THEME_STYLES: Dict[str, ThemeStyle] = {
    "CUSTOM": {
        "wall": cast(str, COLORS["PALETTE_WALL"]),
        "path": cast(str, COLORS["PALETTE_PATH"]),
        "pattern": cast(str, COLORS["PALETTE_PATTERN"]),
        "pattern_display": "  ",
    },
    "MAGENTA": {
        "wall": cast(str, COLORS["MAGENTA_WALL"]),
        "path": cast(str, COLORS["MAGENTA_PATH"]),
        "pattern": cast(str, COLORS["MAGENTA_PATTERN"]),
        "pattern_display": "  ",
    },
    "PASTEL": {
        "wall": cast(str, COLORS["PASTEL_WALL"]),
        "path": cast(str, COLORS["PASTEL_PATH"]),
        "pattern": cast(str, COLORS["PASTEL_PATTERN"]),
        "pattern_display": "  ",
    },
    "NEON": {
        "wall": cast(str, COLORS["NEON_WALL"]),
        "path": cast(str, COLORS["NEON_PATH"]),
        "pattern": cast(str, COLORS["NEON_PATTERN"]),
        "pattern_display": "  ",
    },
}

THEME_CYCLE: List[str] = [
    "CUSTOM",
    "MAGENTA",
    "PASTEL",
    "NEON",
]
DEFAULT_THEME = "CUSTOM"


def build_path_cells(maze_gen: Any) -> List[Tuple[int, int]]:
    """Build ordered list of path cells from entry to exit."""
    ordered_cells: List[Tuple[int, int]] = []
    if not hasattr(maze_gen, 'solution') or not maze_gen.solution:
        return ordered_cells
    cx, cy = maze_gen.entry
    ordered_cells.append((cx, cy))
    directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    for move in maze_gen.solution:
        if move in directions:
            dx, dy = directions[move]
            cx += dx
            cy += dy
            ordered_cells.append((cx, cy))
    return ordered_cells


def _get_gradient_color(x: int, y: int, width: int, height: int) -> str:
    """Return a gradient rainbow color based on position."""
    gradient = cast(List[str], COLORS["RAINBOW_GRADIENT"])
    total = width + height
    index = int(((x + y) / total) * len(gradient))
    index = min(index, len(gradient) - 1)
    return gradient[index]


def render(
    maze_gen: Any,
    show_path: bool = False,
    theme_name: str = DEFAULT_THEME,
    path_reveal_count: Optional[int] = None,
) -> str:
    """Generate a pixel-art block representation of the maze."""
    style = THEME_STYLES.get(theme_name, THEME_STYLES[DEFAULT_THEME])

    reset_color = cast(str, COLORS["RESET"])
    entry_def_color = cast(str, COLORS["ENTRY"])
    exit_def_color = cast(str, COLORS["EXIT"])

    if theme_name == "CUSTOM":
        bg_empty = cast(str, COLORS["PALETTE_BG"]) + "  "
        entry_color = entry_def_color + "  "
        exit_color = exit_def_color + "  "
    elif theme_name == "MAGENTA":
        bg_empty = cast(str, COLORS["MAGENTA_BG"]) + "  "
        entry_color = entry_def_color + "  "
        exit_color = exit_def_color + "  "
    elif theme_name == "PASTEL":
        bg_empty = cast(str, COLORS["PASTEL_BG"]) + "  "
        entry_color = cast(str, COLORS["PASTEL_START_END"]) + "  "
        exit_color = cast(str, COLORS["PASTEL_START_END"]) + "  "
    elif theme_name == "NEON":
        bg_empty = cast(str, COLORS["NEON_BG"]) + "  "
        entry_color = cast(str, COLORS["NEON_START"]) + "  "
        exit_color = cast(str, COLORS["NEON_EXIT"]) + "  "
    else:
        bg_empty = reset_color + "  "
        entry_color = entry_def_color + "  "
        exit_color = exit_def_color + "  "

    path_cells: Set[Tuple[int, int]] = set()
    if show_path and hasattr(maze_gen, 'solution') and maze_gen.solution:
        ordered_path = build_path_cells(maze_gen)
        limit = (
            len(ordered_path)
            if path_reveal_count is None
            else path_reveal_count
        )
        path_cells = set(ordered_path[:limit])

    render_width = maze_gen.width * 2 + 1
    render_height = maze_gen.height * 2 + 1
    display_grid = [
        ["WALL" for _ in range(render_width)]
        for _ in range(render_height)
    ]

    pattern_cells: Set[Tuple[int, int]] = set()
    if hasattr(maze_gen, '_maze') and hasattr(maze_gen._maze, 'pattern_cells'):
        pattern_cells = maze_gen._maze.pattern_cells
    elif hasattr(maze_gen, 'pattern_cells'):
        pattern_cells = maze_gen.pattern_cells

    for y in range(maze_gen.height):
        for x in range(maze_gen.width):
            rx = x * 2 + 1
            ry = y * 2 + 1
            cell_mask = maze_gen.grid[y][x]
            pos = (x, y)
            is_pattern = pos in pattern_cells

            if pos == maze_gen.entry:
                cell_color = entry_color
            elif pos == maze_gen.exit_:
                cell_color = exit_color
            elif show_path and pos in path_cells:
                cell_color = style["path"] + "  "
            elif is_pattern:
                cell_color = style["pattern"] + style["pattern_display"]
            else:
                cell_color = bg_empty

            display_grid[ry][rx] = cell_color

            if not (cell_mask & 2) and (x + 1 < maze_gen.width):
                east_pos = (x + 1, y)
                is_east_pattern = east_pos in pattern_cells

                if is_pattern and is_east_pattern:
                    display_grid[ry][rx + 1] = (
                        style["pattern"] + style["pattern_display"]
                    )
                elif (
                    show_path
                    and pos in path_cells
                    and east_pos in path_cells
                ):
                    display_grid[ry][rx + 1] = style["path"] + "  "
                else:
                    display_grid[ry][rx + 1] = bg_empty

            if not (cell_mask & 4) and (y + 1 < maze_gen.height):
                south_pos = (x, y + 1)
                is_south_pattern = south_pos in pattern_cells

                if is_pattern and is_south_pattern:
                    display_grid[ry + 1][rx] = (
                        style["pattern"] + style["pattern_display"]
                    )
                elif (
                    show_path
                    and pos in path_cells
                    and south_pos in path_cells
                ):
                    display_grid[ry + 1][rx] = style["path"] + "  "
                else:
                    display_grid[ry + 1][rx] = bg_empty

    for y in range(render_height):
        for x in range(render_width):
            if display_grid[y][x] == "WALL":
                if theme_name == "RAINBOW":
                    wall_color = _get_gradient_color(
                        x, y, render_width, render_height
                    )
                else:
                    wall_color = style["wall"]
                display_grid[y][x] = wall_color + "  "

    final_lines = []
    for row in display_grid:
        final_lines.append("".join(row) + reset_color)

    return "\n".join(final_lines)
