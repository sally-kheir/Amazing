from __future__ import annotations
from typing import Iterator, Tuple, Set, Optional

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

class Maze:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.entry: Optional[Tuple[int, int]] = None
        self.exit_: Optional[Tuple[int, int]] = None
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height


    def is_wall(self, x: int, y: int, direction: int) -> bool:
        if not self.in_bounds(x, y):
            return False
        return bool(self.grid[y][x] & direction)


    def open_wall(self, x: int, y: int, direction: int) -> None:
        if not self.in_bounds(x, y):
            return
        self.grid[y][x] &= ~direction

        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy

        if self.in_bounds(nx, ny):
            self.grid[ny][nx] &= ~OPPOSITE[direction]


    def neighbours(self, x: int, y: int) -> Iterator[Tuple[int, int, int]]:
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and (nx, ny) not in self.pattern_cells:
                yield(direction,nx, ny)
            