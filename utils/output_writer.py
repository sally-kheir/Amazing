# utils/output_writer.py
import sys
from typing import Any


def write_output(maze_gen: Any, filepath: str) -> None:
    """Écrit la structure du labyrinthe au format hexadécimal standardisé.

    Args:
        maze_gen: L'instance du MazeGenerator de Danah.
        filepath: Le chemin du fichier de sortie.
    """
    try:
        with open(filepath, 'w') as f:
            # Écriture de la grille au format Hexa
            for row in maze_gen.grid:
                row_str = "".join(f"{cell:X}" for cell in row)
                f.write(f"{row_str}\n")

            # Ligne vide obligatoire
            f.write("\n")

            # Métadonnées et chemin le plus court formaté sans crochets ni
            # virgules
            f.write(f"{maze_gen.entry[0]},{maze_gen.entry[1]}\n")
            f.write(f"{maze_gen.exit_[0]},{maze_gen.exit_[1]}\n")

            solution_str = "".join(
                maze_gen.solution) if maze_gen.solution else ""
            f.write(f"{solution_str}\n")

    except IOError as e:
        print(f"Error writing to output file {filepath}: {e}", file=sys.stderr)
