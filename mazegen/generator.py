from __future__ import annotations
import random
from typing import Optional, Tuple
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST, DELTA, OPPOSITE


class MazeGenerator:

    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self._maze = Maze(width, height)
        self.grid = None
        self.entry: Optional[Tuple[int, int]] = None
        self.exit_: Optional[Tuple[int, int]] = None
        self.solution: Optional[str] = None

    def generate(self, entry: Tuple[int, int], exit_: Tuple[int, int], perfect: bool = True) -> None:
        # 1. set random seed if self.seed is not None
        self.seed = 42
        # 2. reset the maze grid
        self._maze = Maze(self.width, self.height)
        
        # 3. inject 42 pattern (import and call from pattern.py later)
        # for now skip this line

        # 4. set up stack and visited set starting at entry
        
        # 5. while loop — recursive backtracker
        
        # 6. store results
        self.grid = self._maze.grid
        self.entry = entry
        self.exit_ = exit_
        # self.solution = find_path(...) ← we'll add this after pathfinder.py