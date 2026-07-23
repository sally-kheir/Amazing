# display/ascii_view.py
from typing import Any, Set, Tuple, Dict, List, Optional, TypedDict


COLORS = {
    "RESET": "\033[0m",
    
    # Entry/Exit colors
    "ENTRY": "\033[48;5;201m",   # Bright pink for entry
    "EXIT": "\033[48;5;117m",    # Light blue for exit
    
    # Strawberry theme — PASTEL PINK walls (not hot pink, not peachy!)
    "STRAWBERRY_WALL": "\033[48;5;218m",   # Pastel pink ✅ (soft, light pink)
    "STRAWBERRY_PATH": "\033[48;5;196m",   # Bright red
    "STRAWBERRY_PATTERN": "\033[48;5;196m", # Red pattern blocks
    
    # Lilac theme
    "LILAC_WALL": "\033[48;5;189m",        # Soft lilac
    "LILAC_PATH": "\033[48;5;54m",         # Dark purple
    "LILAC_PATTERN": "\033[48;5;54m",      # Dark purple pattern
    
    # Rainbow theme — grey walls, grey path, grey 42
    "RAINBOW_GREY": "\033[48;5;240m",      # Dark grey
    "RAINBOW_PATH": "\033[48;5;240m",      # Grey path
    "RAINBOW_PATTERN": "\033[48;5;240m",   # Grey 42 pattern
    
    # 42 Theme — LIGHTER BLUE 42, grey walls, lighter blue path
    "FORTYTWO_WALL": "\033[48;5;240m",     # Grey walls
    "FORTYTWO_PATH": "\033[48;5;75m",      # Lighter blue
    "FORTYTWO_PATTERN": "\033[48;5;75m",   # Lighter blue 42 pattern
    
    # Gradient colors for rainbow walls
    "RAINBOW_GRADIENT": [
        "\033[48;5;196m",   # Red
        "\033[48;5;202m",   # Orange-red
        "\033[48;5;208m",   # Orange
        "\033[48;5;214m",   # Yellow-orange
        "\033[48;5;226m",   # Yellow
        "\033[48;5;118m",   # Yellow-green
        "\033[48;5;46m",    # Green
        "\033[48;5;51m",    # Cyan
        "\033[48;5;21m",    # Blue
        "\033[48;5;57m",    # Indigo
        "\033[48;5;93m",    # Violet
        "\033[48;5;165m",   # Purple
    ],
}


class ThemeStyle(TypedDict):
    """Full style associated with a theme."""

    wall: str
    path: str
    pattern: str
    pattern_display: str  # What to display for pattern cells


THEME_STYLES: Dict[str, ThemeStyle] = {
    "STRAWBERRY": {
        "wall": COLORS["STRAWBERRY_WALL"],
        "path": COLORS["STRAWBERRY_PATH"],
        "pattern": COLORS["STRAWBERRY_PATTERN"],
        "pattern_display": "\U0001F353",  # 🍓 - ALL pattern cells show this
    },
    "LILAC": {
        "wall": COLORS["LILAC_WALL"],
        "path": COLORS["LILAC_PATH"],
        "pattern": COLORS["LILAC_PATTERN"],
        "pattern_display": "\U0001F338",  # 🌸 - ALL pattern cells show this
    },
    "RAINBOW": {
        "wall": COLORS["RAINBOW_GREY"],
        "path": COLORS["RAINBOW_PATH"],
        "pattern": COLORS["RAINBOW_PATTERN"],
        "pattern_display": "  ",  # Empty space - ALL pattern cells are solid grey
    },
    "42": {
        "wall": COLORS["FORTYTWO_WALL"],
        "path": COLORS["FORTYTWO_PATH"],
        "pattern": COLORS["FORTYTWO_PATTERN"],
        "pattern_display": "  ",  # Empty space - ALL pattern cells are solid blue
    },
}

# Theme cycle order
THEME_CYCLE: List[str] = ["STRAWBERRY", "LILAC", "RAINBOW", "42"]
DEFAULT_THEME = "STRAWBERRY"


def build_path_cells(maze_gen: Any) -> List[Tuple[int, int]]:
    """Build ordered list of path cells from entry to exit."""
    ordered_cells: List[Tuple[int, int]] = []
    if not maze_gen.solution:
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
    gradient = COLORS["RAINBOW_GRADIENT"]
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
    bg_empty = COLORS["RESET"] + "  "
    style = THEME_STYLES.get(theme_name, THEME_STYLES[DEFAULT_THEME])

    # Build path cells set if needed
    path_cells: Set[Tuple[int, int]] = set()
    if show_path and maze_gen.solution:
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

    # Get pattern cells
    has_pattern = hasattr(maze_gen, '_maze') and hasattr(maze_gen._maze, 'pattern_cells')
    pattern_cells = set()
    if has_pattern:
        pattern_cells = maze_gen._maze.pattern_cells

    for y in range(maze_gen.height):
        for x in range(maze_gen.width):
            rx = x * 2 + 1
            ry = y * 2 + 1
            cell_mask = maze_gen.grid[y][x]
            pos = (x, y)
            is_pattern = pos in pattern_cells

            # Determine cell content
            if pos == maze_gen.entry:
                cell_color = COLORS["ENTRY"] + "  "
            elif pos == maze_gen.exit_:
                cell_color = COLORS["EXIT"] + "  "
            elif show_path and pos in path_cells:
                cell_color = style["path"] + "  "
            elif is_pattern:
                # ALL pattern cells use the SAME display!
                cell_color = style["pattern"] + style["pattern_display"]
            else:
                cell_color = bg_empty

            display_grid[ry][rx] = cell_color

            # Open east passage
            if not (cell_mask & 2) and (x + 1 < maze_gen.width):
                east_pos = (x + 1, y)
                is_east_pattern = east_pos in pattern_cells
                
                if is_pattern and is_east_pattern:
                    # Both pattern cells - use pattern display
                    display_grid[ry][rx + 1] = style["pattern"] + style["pattern_display"]
                elif (
                    show_path
                    and pos in path_cells
                    and east_pos in path_cells
                ):
                    display_grid[ry][rx + 1] = style["path"] + "  "
                else:
                    display_grid[ry][rx + 1] = bg_empty

            # Open south passage
            if not (cell_mask & 4) and (y + 1 < maze_gen.height):
                south_pos = (x, y + 1)
                is_south_pattern = south_pos in pattern_cells
                
                if is_pattern and is_south_pattern:
                    # Both pattern cells - use pattern display
                    display_grid[ry + 1][rx] = style["pattern"] + style["pattern_display"]
                elif (
                    show_path
                    and pos in path_cells
                    and south_pos in path_cells
                ):
                    display_grid[ry + 1][rx] = style["path"] + "  "
                else:
                    display_grid[ry + 1][rx] = bg_empty

    # Paint wall blocks
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
        final_lines.append("".join(row) + COLORS["RESET"])

    return "\n".join(final_lines)