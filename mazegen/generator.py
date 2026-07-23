from __future__ import annotations
import random
from typing import Optional, Tuple
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST
from mazegen.pathfinder import find_path
from mazegen.pattern import inject_42
import sys


class MazeGenerator:
    """Generates mazes using recursive backtracker algorithm."""

    def __init__(
            self,
            width: int,
            height: int,
            seed: Optional[int] = None) -> None:
        """Initialize generator with maze dimensions and optional seed."""
        self.width = width
        self.height = height
        self.seed = seed
        # Indique si la premiere generation a deja eu lieu. La seed n'est
        # appliquee QUE lors de ce premier appel, pour garantir la
        # reproductibilite demandee par le sujet (IV.4), tout en laissant
        # les regenerations suivantes (menu "1") produire un vrai nouveau
        # labyrinthe a chaque fois.
        self._first_generation = True
        self._maze = Maze(width, height)
        self.grid = None
        self.entry: Optional[Tuple[int, int]] = None
        self.exit_: Optional[Tuple[int, int]] = None
        self.solution: Optional[str] = None

    def _fix_open_areas(self) -> None:
        """Ensure no 3x3 fully open area exists in the maze."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                # Check if all internal walls in this 3x3 window are open
                fully_open = True
                for row in range(y, y + 3):
                    for col in range(x, x + 3):
                        if (col, row) in self._maze.pattern_cells:
                            fully_open = False
                            break
                        # Check east wall (except last column of window)
                        if col < x + 2:
                            if self._maze.is_wall(col, row, EAST):
                                fully_open = False
                                break
                        # Check south wall (except last row of window)
                        if row < y + 2:
                            if self._maze.is_wall(col, row, SOUTH):
                                fully_open = False
                                break
                    if not fully_open:
                        break
                if fully_open:
                    # Close the south wall of the center cell
                    cx, cy = x + 1, y + 1
                    self._maze.grid[cy][cx] |= SOUTH
                    self._maze.grid[cy + 1][cx] |= NORTH

    def generate(self,
                 entry: Tuple[int,
                              int],
                 exit_: Tuple[int,
                              int],
                 perfect: bool = True) -> None:
        """Generate a maze using recursive backtracker."""

        # 1. Set random seed for reproducibility -- uniquement au premier appel
        if self.seed is not None and self._first_generation:
            random.seed(self.seed)
            self._first_generation = False

        # 2. Reset maze and inject 42 pattern
        self._maze = Maze(self.width, self.height)
        inject_42(self._maze)

        # Store entry/exit
        self.entry = entry
        self.exit_ = exit_

        # Open the border wall at entry and exit
        # so the player can enter and exit the maze
        ex, ey = entry
        if ex == 0:
            self._maze.grid[ey][ex] &= ~WEST
        elif ex == self.width - 1:
            self._maze.grid[ey][ex] &= ~EAST
        elif ey == 0:
            self._maze.grid[ey][ex] &= ~NORTH
        elif ey == self.height - 1:
            self._maze.grid[ey][ex] &= ~SOUTH

        xx, xy = exit_
        if xx == 0:
            self._maze.grid[xy][xx] &= ~WEST
        elif xx == self.width - 1:
            self._maze.grid[xy][xx] &= ~EAST
        elif xy == 0:
            self._maze.grid[xy][xx] &= ~NORTH
        elif xy == self.height - 1:
            self._maze.grid[xy][xx] &= ~SOUTH

        # 3. Recursive backtracker
        stack = [entry]
        visited = {entry}
        total_cells = (self.width * self.height) - \
            len(self._maze.pattern_cells)

        while stack and len(visited) < total_cells:
            x, y = stack[-1]  # Peek at current cell

            # Find unvisited neighbours (using visited set)
            unvisited = []
            for direction, nx, ny in self._maze.neighbours(x, y):
                if (nx, ny) not in visited:
                    unvisited.append((direction, nx, ny))

            if unvisited:
                # Pick one randomly
                direction, nx, ny = random.choice(unvisited)
                # Knock down the wall
                self._maze.open_wall(x, y, direction)
                # Move into it
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                # Backtrack
                stack.pop()

        # 4. If not perfect, add some loops
        if not perfect:
            self._add_loops()

        self._fix_open_areas()
        # 5. Store results
        self.grid = self._maze.grid
        self.solution = find_path(self._maze, entry, exit_)

    def _add_loops(self) -> None:
        """Add loops to make maze non-perfect."""
        # Get all cells that are not pattern cells
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self._maze.pattern_cells:
                    cells.append((x, y))

        # Randomly open some walls between already-connected cells
        attempts = min(10, len(cells) // 5)
        for _ in range(attempts):
            x, y = random.choice(cells)
            # Find neighbours with walls
            walled_neighbours = []
            for direction, nx, ny in self._maze.neighbours(x, y):
                if self._maze.is_wall(x, y, direction):
                    walled_neighbours.append((direction, nx, ny))

            if walled_neighbours:
                direction, nx, ny = random.choice(walled_neighbours)
                self._maze.open_wall(x, y, direction)

    def get_maze(self) -> Maze:
        """Return the internal Maze object."""
        return self._maze
