from __future__ import annotations
from mazegen.maze import Maze

MIN_WIDTH_FOR_42 = 7
MIN_HEIGHT_FOR_42 = 5


def inject_42(maze: Maze) -> bool:
    """Inject the 42 pattern into the maze.

    Carves out the shape of the number "42" as a block of fully
    closed (isolated) cells within the maze grid, centered as
    closely as possible within the given dimensions.

    Args:
        maze: The Maze instance to modify in place.

    Returns:
        True if the pattern was successfully injected, False if the
        maze is too small (width < MIN_WIDTH_FOR_42 or
        height < MIN_HEIGHT_FOR_42) to fit the pattern.
    """
    if maze.width < MIN_WIDTH_FOR_42 or maze.height < MIN_HEIGHT_FOR_42:
        print(
            f"Maze too small to display 42 pattern "
            f"(minimum size: {MIN_WIDTH_FOR_42}x{MIN_HEIGHT_FOR_42}, "
            f"got {maze.width}x{maze.height})"
        )
        return False

    cx = (maze.width - MIN_WIDTH_FOR_42) // 2
    cy = (maze.height - MIN_HEIGHT_FOR_42) // 2

    shape_4 = [
        (0, 0), (2, 0),
        (0, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
        (2, 3),
        (2, 4),
    ]

    shape_2 = [
        (4, 0), (5, 0), (6, 0),
        (6, 1),
        (4, 2), (5, 2), (6, 2),
        (4, 3),
        (4, 4), (5, 4), (6, 4),
    ]

    all_pattern_cells = []
    for offset_x, offset_y in shape_4:
        px = cx + offset_x
        py = cy + offset_y
        all_pattern_cells.append((px, py))

    for offset_x, offset_y in shape_2:
        px = cx + offset_x
        py = cy + offset_y
        all_pattern_cells.append((px, py))

    maze.pattern_cells = set(all_pattern_cells)

    for px, py in maze.pattern_cells:
        maze.grid[py][px] = 15

    return True
