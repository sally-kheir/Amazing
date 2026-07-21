from __future__ import annotations
import random
from typing import Optional, Tuple
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST, DELTA, OPPOSITE
from mazegen.pathfinder import find_path
from mazegen.pattern import inject_42


class MazeGenerator:
    """Generates mazes using recursive backtracker algorithm."""

    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
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

    def generate(self, entry: Tuple[int, int], exit_: Tuple[int, int], perfect: bool = True) -> None:
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

        # 3. Recursive backtracker
        stack = [entry]
        visited = {entry}
        total_cells = (self.width * self.height) - len(self._maze.pattern_cells)

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