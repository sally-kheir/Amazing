import sys
from typing import Any


def write_output(maze_gen: Any, filepath: str) -> None:
    """Writes the maze structure in standardized hexadecimal format.

    Args:
        maze_gen: The MazeGenerator instance
           filepath: The path to the output file.
    """
    try:
        with open(filepath, 'w') as f:
            for row in maze_gen.grid:
                row_str = "".join(f"{cell:X}" for cell in row)
                f.write(f"{row_str}\n")

            f.write("\n")

            f.write(f"{maze_gen.entry[0]},{maze_gen.entry[1]}\n")
            f.write(f"{maze_gen.exit_[0]},{maze_gen.exit_[1]}\n")

            solution_str = "".join(
                maze_gen.solution) if maze_gen.solution else ""
            f.write(f"{solution_str}\n")

    except IOError as e:
        print(f"Error writing to output file {filepath}: {e}", file=sys.stderr)
