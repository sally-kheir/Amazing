from __future__ import annotations
from collections import deque
from typing import Deque, Dict, Optional, Tuple
from mazegen.maze import Maze


def find_path(
        maze: Maze, entry: Tuple[int, int], exit_: Tuple[int, int]) -> str:

    if entry == exit_:
        return ""

    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {entry: None}
    queue: Deque[Tuple[int, int]] = deque([entry])

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit_:
            break

        for direction, nx, ny in maze.neighbours(x, y):
            if not maze.is_wall(x, y, direction):
                if (nx, ny) not in came_from:
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    if exit_ not in came_from:
        return ""

    path = []
    current = exit_

    while current != entry:
        prev = came_from[current]
        if prev is None:
            break
        dx = current[0] - prev[0]
        dy = current[1] - prev[1]
        if dx == 1:
            path.append('E')
        elif dx == -1:
            path.append('W')
        elif dy == 1:
            path.append('S')
        elif dy == -1:
            path.append('N')
        current = prev

    path.reverse()
    return ''.join(path)
