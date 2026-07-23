# mazegen/pattern.py
from __future__ import annotations
from mazegen.maze import Maze


def inject_42(maze: Maze) -> bool:
    """Inject the 42 pattern into the maze."""
    if maze.width < 7 or maze.height < 5:
        print("Maze too small to display 42 pattern")
        return False
    
    cx = (maze.width - 7) // 2
    cy = (maze.height - 5) // 2

    # Shape of '4' - ALL cells that form the number 4
    shape_4 = [
        (0, 0), (2, 0),      # top row
        (0, 1), (2, 1),      # second row
        (0, 2), (1, 2), (2, 2),   # middle row (horizontal bar)
        (2, 3),              # fourth row
        (2, 4),              # bottom row
    ]

    # Shape of '2' - ALL cells that form the number 2
    shape_2 = [
        (4, 0), (5, 0), (6, 0),   # top row (horizontal bar)
        (6, 1),                    # second row (right side)
        (4, 2), (5, 2), (6, 2),   # middle row (horizontal bar)
        (4, 3),                    # fourth row (left side)
        (4, 4), (5, 4), (6, 4),   # bottom row (horizontal bar)
    ]

    # Add ALL pattern cells to the set
    all_pattern_cells = []
    for offset_x, offset_y in shape_4:
        px = cx + offset_x
        py = cy + offset_y
        all_pattern_cells.append((px, py))
    
    for offset_x, offset_y in shape_2:
        px = cx + offset_x
        py = cy + offset_y
        all_pattern_cells.append((px, py))
    
    # Store ALL pattern cells in the maze
    maze.pattern_cells = set(all_pattern_cells)
    
    # Make ALL pattern cells fully closed (15)
    for px, py in maze.pattern_cells:
        maze.grid[py][px] = 15

    return True