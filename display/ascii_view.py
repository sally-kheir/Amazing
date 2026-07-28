# display/ascii_view.py
from typing import Any, Set, Tuple, Dict, List, Optional, TypedDict


COLORS = {
    "RESET": "\033[0m",
    
    # Entry/Exit default colors (#CCE092)
    "ENTRY": "\033[48;2;204;224;146m",   # #CCE092
    "EXIT": "\033[48;2;204;224;146m",    # #CCE092
    
    # Palette Hex (Theme Custom)
    "PALETTE_WALL": "\033[48;2;186;176;149m",     # #BAB095
    "PALETTE_PATH": "\033[48;2;204;224;146m",     # #CCE092
    "PALETTE_BG": "\033[48;2;237;232;208m",       # #EDE8D0
    "PALETTE_PATTERN": "\033[48;2;214;211;154m",  # #D6D39A

    # Palette Hex (Theme Magenta)
    "MAGENTA_WALL": "\033[48;2;103;0;103m",       # #670067
    "MAGENTA_BG": "\033[48;2;255;173;255m",       # #FFADFF
    "MAGENTA_PATH": "\033[48;2;167;69;214m",     # #A745D6
    "MAGENTA_PATTERN": "\033[48;2;193;28;132m",   # #C11C84

    # Palette Hex (Theme Pastel)
    "PASTEL_WALL": "\033[48;2;216;164;181m",      # #D8A4B5
    "PASTEL_BG": "\033[48;2;242;231;189m",        # #F2E7BD
    "PASTEL_PATH": "\033[48;2;189;217;242m",      # #BDD9F2
    "PASTEL_PATTERN": "\033[48;2;242;189;205m",   # #F2BDCD
    "PASTEL_START_END": "\033[48;2;225;242;189m", # #E1F2BD

    # Palette Hex (Theme Neon Pastel)
    "NEON_WALL": "\033[48;2;184;92;207m",         # #B85CCF (Murs)
    "NEON_BG": "\033[48;2;255;179;243m",          # #FFB3F3 (Fond)
    "NEON_PATH": "\033[48;2;115;255;223m",        # #73FFDF (Chemin)
    "NEON_PATTERN": "\033[48;2;223;115;255m",     # #DF73FF (Motif 42)
    "NEON_START": "\033[48;2;255;115;215m",       # #FF73D7 (Début)
    "NEON_EXIT": "\033[48;2;175;255;237m",        # #AFFFED (Fin)

    # Strawberry theme
    "STRAWBERRY_WALL": "\033[48;5;218m",   
    "STRAWBERRY_PATH": "\033[48;5;196m",   
    "STRAWBERRY_PATTERN": "\033[48;5;196m", 
    
    # Lilac theme
    "LILAC_WALL": "\033[48;5;189m",        
    "LILAC_PATH": "\033[48;5;54m",         
    "LILAC_PATTERN": "\033[48;5;54m",      
    
    # Rainbow theme
    "RAINBOW_GREY": "\033[48;5;240m",      
    "RAINBOW_PATH": "\033[48;5;240m",      
    "RAINBOW_PATTERN": "\033[48;5;240m",   
    
    # 42 Theme
    "FORTYTWO_WALL": "\033[48;5;240m",     
    "FORTYTWO_PATH": "\033[48;5;75m",      
    "FORTYTWO_PATTERN": "\033[48;5;75m",   
    
    # Gradient colors for rainbow walls
    "RAINBOW_GRADIENT": [
        "\033[48;5;196m",
        "\033[48;5;202m",
        "\033[48;5;208m",
        "\033[48;5;214m",
        "\033[48;5;226m",
        "\033[48;5;118m",
        "\033[48;5;46m",
        "\033[48;5;51m",
        "\033[48;5;21m",
        "\033[48;5;57m",
        "\033[48;5;93m",
        "\033[48;5;165m",
    ],
}


class ThemeStyle(TypedDict):
    """Full style associated with a theme."""

    wall: str
    path: str
    pattern: str
    pattern_display: str


THEME_STYLES: Dict[str, ThemeStyle] = {
    "CUSTOM": {
        "wall": COLORS["PALETTE_WALL"],
        "path": COLORS["PALETTE_PATH"],
        "pattern": COLORS["PALETTE_PATTERN"],
        "pattern_display": "  ",
    },
    "MAGENTA": {
        "wall": COLORS["MAGENTA_WALL"],
        "path": COLORS["MAGENTA_PATH"],
        "pattern": COLORS["MAGENTA_PATTERN"],
        "pattern_display": "  ",
    },
    "PASTEL": {
        "wall": COLORS["PASTEL_WALL"],
        "path": COLORS["PASTEL_PATH"],
        "pattern": COLORS["PASTEL_PATTERN"],
        "pattern_display": "  ",
    },
    "NEON": {
        "wall": COLORS["NEON_WALL"],
        "path": COLORS["NEON_PATH"],
        "pattern": COLORS["NEON_PATTERN"],
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
    style = THEME_STYLES.get(theme_name, THEME_STYLES[DEFAULT_THEME])

    if theme_name == "CUSTOM":
        bg_empty = COLORS["PALETTE_BG"] + "  "
        entry_color = COLORS["ENTRY"] + "  "
        exit_color = COLORS["EXIT"] + "  "
    elif theme_name == "MAGENTA":
        bg_empty = COLORS["MAGENTA_BG"] + "  "
        entry_color = COLORS["ENTRY"] + "  "
        exit_color = COLORS["EXIT"] + "  "
    elif theme_name == "PASTEL":
        bg_empty = COLORS["PASTEL_BG"] + "  "
        entry_color = COLORS["PASTEL_START_END"] + "  "
        exit_color = COLORS["PASTEL_START_END"] + "  "
    elif theme_name == "NEON":
        bg_empty = COLORS["NEON_BG"] + "  "
        entry_color = COLORS["NEON_START"] + "  "
        exit_color = COLORS["NEON_EXIT"] + "  "
    else:
        bg_empty = COLORS["RESET"] + "  "
        entry_color = COLORS["ENTRY"] + "  "
        exit_color = COLORS["EXIT"] + "  "

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
                    display_grid[ry][rx + 1] = style["pattern"] + style["pattern_display"]
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
                    display_grid[ry + 1][rx] = style["pattern"] + style["pattern_display"]
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
        final_lines.append("".join(row) + COLORS["RESET"])

    return "\n".join(final_lines)