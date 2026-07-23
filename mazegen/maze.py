from __future__ import annotations
from typing import Iterator, Tuple, Set, Optional

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}


class Maze:
    """Grid-based maze with walls stored as per-cell bitmasks.

    Each cell stores a 4-bit integer where each bit represents
    a wall direction: North=1, East=2, South=4, West=8.
    A bit set to 1 means that wall is closed.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize maze with all walls closed.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
        """
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.entry: Optional[Tuple[int, int]] = None
        self.exit_: Optional[Tuple[int, int]] = None
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within the maze boundaries.

        Args:
            x: The column index.
            y: The row index.

        Returns:
            True if (x, y) is a valid cell coordinate, False otherwise.
        """
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def is_wall(self, x: int, y: int, direction: int) -> bool:
        """Check if a wall exists on a given side of a cell.

        Args:
            x: The column index of the cell.
            y: The row index of the cell.
            direction: One of NORTH, EAST, SOUTH, WEST constants.

        Returns:
            True if the wall is closed, False if open or out of bounds.
        """
        if not self.in_bounds(x, y):
            return False
        return bool(self.grid[y][x] & direction)

    def open_wall(self, x: int, y: int, direction: int) -> None:
        """Open the wall between a cell and its neighbour.

        This is the only place wall bits should be cleared.
        Updates both the current cell and the neighbouring cell
        to maintain wall coherence across the maze.

        Args:
            x: The column index of the current cell.
            y: The row index of the current cell.
            direction: The direction of the wall to open.
        """
        if not self.in_bounds(x, y):
            return
        self.grid[y][x] &= ~direction
        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy
        if self.in_bounds(nx, ny):
            self.grid[ny][nx] &= ~OPPOSITE[direction]

    def neighbours(self, x: int, y: int) -> Iterator[Tuple[int, int, int]]:
        """Yield all valid neighbours of a cell.

        Skips neighbours that are out of bounds or part of
        the 42 pattern cells.

        Args:
            x: The column index of the cell.
            y: The row index of the cell.

        Yields:
            Tuples of (direction, nx, ny) for each valid neighbour.
        """
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and (nx, ny) not in self.pattern_cells:
                yield direction, nx, ny
