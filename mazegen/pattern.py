from __future__ import annotations
from mazegen.maze import Maze


def inject_42(maze: Maze) -> bool:

    if maze.width < 7 or maze.height < 5:
        print("Maze too small to display 42 pattern")
        return False
    
    cx = (maze.width - 7) // 2
    cy = (maze.height - 5) // 2

    shape_4 = [
        (0, 0), (2, 0),   # row 0
        (0, 1), (2, 1),   # row 1
        (0, 2), (1, 2), (2, 2),   # row 2
        (2, 3),           # row 3
        (2, 4),           # row 4
    ]

    shape_2 = [
        (4, 0), (5, 0), (6, 0),   # row 0
        (6, 1),                    # row 1
        (4, 2), (5, 2), (6, 2),   # row 2
        (4, 3),                    # row 3
        (4, 4), (5, 4), (6, 4),   # row 4
    ]

    for offset_x, offset_y in shape_4 + shape_2:
        px = cx + offset_x
        py = cy + offset_y
        maze.pattern_cells.add((px, py))
        maze.grid[py][px] = 15

    return True