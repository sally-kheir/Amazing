# display/ascii_view.py
from typing import Any, Set, Tuple, Dict, List, Optional, TypedDict

# Codes ANSI de fond colore (48;5;...m) pour faire des blocs pleins "Pixel Art"
COLORS = {
    "RESET": "\033[0m",
    "ENTRY": "\033[48;5;201m",          # Rose/Magenta vif pour l'entree
    "EXIT": "\033[48;5;117m",           # Bleu ciel pour la sortie

    # Couleurs de murs
    "WHITE": "\033[48;5;231m",          # Blanc pur
    "BABY_PINK": "\033[48;5;224m",      # Rose bebe / rose tres clair
    "LILAC": "\033[48;5;189m",          # Lilas clair
    "BEIGE_ORANGE": "\033[48;5;215m",   # Beige orange / peche clair
    "RED": "\033[48;5;196m",            # Rouge vif (drapeau Liban)

    # Couleurs de chemin (PATH), une par theme
    "PINK_DARK": "\033[48;5;162m",      # Rose fonce
    "DARK_VIOLET": "\033[48;5;54m",     # Violet fonce
    "ORANGE": "\033[48;5;208m",         # Orange vif
    "GOLD": "\033[48;5;178m",           # Dore, pour le theme Liban

    # Couleur pleine pour le motif 42 du theme Liban (cedre vert)
    "CEDAR_GREEN": "\033[48;5;22m",

    # Fond derriere les emojis du motif 42
    "PATTERN_BG": "\033[48;5;233m",     # Fond sombre discret
}


class ThemeStyle(TypedDict):
    """Style complet associe a un theme."""
    wall1: str
    wall2: str
    path: str
    pattern_type: str          # "emoji" ou "solid"
    pattern_value: str         # emoji unicode si "emoji", code couleur ANSI si "solid"


# Chaque theme definit : couleurs de murs, couleur du chemin,
# et comment dessiner le motif "42" (emoji ou couleur pleine).
THEME_STYLES: Dict[str, ThemeStyle] = {
    "STRAWBERRY": {
        "wall1": COLORS["WHITE"],
        "wall2": COLORS["BABY_PINK"],
        "path": COLORS["PINK_DARK"],
        "pattern_type": "emoji",
        "pattern_value": "\U0001F353",   # 🍓 fraise
    },
    "LILAC_FLOWER": {
        "wall1": COLORS["WHITE"],
        "wall2": COLORS["LILAC"],
        "path": COLORS["DARK_VIOLET"],
        "pattern_type": "emoji",
        "pattern_value": "\U0001F338",   # 🌸 fleur
    },
    "ORANGE_FLOWER": {
        "wall1": COLORS["WHITE"],
        "wall2": COLORS["BEIGE_ORANGE"],
        "path": COLORS["ORANGE"],
        "pattern_type": "emoji",
        "pattern_value": "\U0001F34A",   # 🍊 orange
    },
    "LEBANON": {
        "wall1": COLORS["RED"],
        "wall2": COLORS["WHITE"],
        "path": COLORS["GOLD"],
        "pattern_type": "solid",
        "pattern_value": COLORS["CEDAR_GREEN"],  # cedre vert, pas d'emoji
    },
}

# Ordre de rotation utilise par l'option "Rotate maze colors" du menu
THEME_CYCLE: List[str] = ["STRAWBERRY", "LILAC_FLOWER", "ORANGE_FLOWER", "LEBANON"]

DEFAULT_THEME = "STRAWBERRY"


def build_path_cells(maze_gen: Any) -> List[Tuple[int, int]]:
    """Reconstruit la liste ORDONNEE des cellules du chemin (entree -> sortie).

    L'ordre est important pour pouvoir reveler le chemin case par case.
    """
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


def _pattern_cell_render(pattern_type: str, pattern_value: str) -> str:
    """Retourne le texte a afficher pour une cellule du motif '42'."""
    if pattern_type == "emoji":
        return COLORS["PATTERN_BG"] + pattern_value
    # "solid" -> pattern_value est directement un code couleur ANSI
    return pattern_value + "  "


def render(
    maze_gen: Any,
    show_path: bool = False,
    theme_name: str = DEFAULT_THEME,
    path_reveal_count: Optional[int] = None,
) -> str:
    """Genere une representation graphique en blocs pleins du labyrinthe.

    Args:
        maze_gen: L'instance du MazeGenerator.
        show_path: Indique s'il faut afficher le chemin le plus court.
        theme_name: Le nom du theme actif (voir THEME_STYLES). Determine
            les couleurs de murs, la couleur du chemin, et comment le
            motif "42" est dessine (emoji ou couleur pleine).
        path_reveal_count: si fourni, seules les N premieres cellules du
            chemin (dans l'ordre entree -> sortie) sont colorees. Permet
            une revelation progressive, case par case. None = chemin
            entier affiche d'un coup.
    """
    bg_empty = COLORS["RESET"] + "  "

    style = THEME_STYLES.get(theme_name, THEME_STYLES[DEFAULT_THEME])
    color1 = style["wall1"]
    color2 = style["wall2"]
    path_color = style["path"]
    pattern_type = style["pattern_type"]
    pattern_value = style["pattern_value"]
    pattern_cell_text = _pattern_cell_render(pattern_type, pattern_value)

    # 1. Reconstruction du chemin le plus court si active
    path_cells: Set[Tuple[int, int]] = set()
    if show_path and maze_gen.solution:
        ordered_path = build_path_cells(maze_gen)
        limit = len(ordered_path) if path_reveal_count is None else path_reveal_count
        path_cells = set(ordered_path[:limit])

    render_width = maze_gen.width * 2 + 1
    render_height = maze_gen.height * 2 + 1

    display_grid = [["WALL" for _ in range(render_width)] for _ in range(render_height)]

    # 2. Sculpture des passages et des espaces vides
    for y in range(maze_gen.height):
        for x in range(maze_gen.width):
            rx = x * 2 + 1
            ry = y * 2 + 1

            cell_mask = maze_gen.grid[y][x]
            pos = (x, y)

            if pos == maze_gen.entry:
                cell_color = COLORS["ENTRY"] + "  "
            elif pos == maze_gen.exit_:
                cell_color = COLORS["EXIT"] + "  "
            elif show_path and pos in path_cells:
                cell_color = path_color + "  "
            elif cell_mask == 15:  # Cellule fermee du Motif 42
                cell_color = pattern_cell_text
            else:
                cell_color = bg_empty

            display_grid[ry][rx] = cell_color

            # Ouvrir le mur Est
            if not (cell_mask & 2) and (x + 1 < maze_gen.width):
                if cell_mask == 15 and maze_gen.grid[y][x + 1] == 15:
                    display_grid[ry][rx + 1] = pattern_cell_text
                elif show_path and pos in path_cells and (x + 1, y) in path_cells:
                    display_grid[ry][rx + 1] = path_color + "  "
                else:
                    display_grid[ry][rx + 1] = bg_empty

            # Ouvrir le mur Sud
            if not (cell_mask & 4) and (y + 1 < maze_gen.height):
                if cell_mask == 15 and maze_gen.grid[y + 1][x] == 15:
                    display_grid[ry + 1][rx] = pattern_cell_text
                elif show_path and pos in path_cells and (x, y + 1) in path_cells:
                    display_grid[ry + 1][rx] = path_color + "  "
                else:
                    display_grid[ry + 1][rx] = bg_empty

    # 3. Application des couleurs sur les blocs de murs restants ("WALL")
    for y in range(render_height):
        for x in range(render_width):
            if display_grid[y][x] == "WALL":
                chosen_wall_color = color1 if (x + y) % 2 == 0 else color2
                display_grid[y][x] = chosen_wall_color + "  "

    # 4. Assemblage final des lignes
    final_lines = []
    for row in display_grid:
        final_lines.append("".join(row) + COLORS["RESET"])

    return "\n".join(final_lines)