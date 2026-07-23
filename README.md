*This project has been created as part of the 42 curriculum by dael-ter, skheir.*

## Description

A-Maze-ing is a maze generator written in Python 3. It takes a configuration
file as input, generates a maze using the recursive backtracker algorithm,
and writes it to an output file using a hexadecimal wall encoding. The maze
is displayed visually in the terminal with interactive controls.

The project includes a reusable `mazegen` Python package that can be installed
via pip and imported independently of the CLI application.

## Instructions

### Requirements
- Python 3.10 or later
- pip

### Installation
```bash
make install
```

### Running
```bash
make run
```
Or directly:
```bash
python3 a_maze_ing.py config.txt
```

### Other commands
```bash
make debug       # run with Python debugger
make clean       # remove cache files
make lint        # run flake8 and mypy
```

## Configuration file format

The config file uses `KEY=VALUE` format, one per line.
Lines starting with `#` are comments and are ignored.

| Key | Description | Example |
|-----|-------------|---------|
| WIDTH | Maze width in cells | WIDTH=20 |
| HEIGHT | Maze height in cells | HEIGHT=15 |
| ENTRY | Entry coordinates x,y | ENTRY=0,0 |
| EXIT | Exit coordinates x,y | EXIT=19,14 |
| OUTPUT_FILE | Output filename | OUTPUT_FILE=maze.txt |
| PERFECT | One path only? | PERFECT=True |
| SEED | Random seed (optional) | SEED=42 |

Example `config.txt`:

- WIDTH=20
- HEIGHT=15
- ENTRY=0,0
- EXIT=19,14
- OUTPUT_FILE=maze.txt
- PERFECT=True
- SEED=42

## Algorithm

We chose the **Recursive Backtracker** algorithm (randomized depth-first search).

How it works:
1. Start at the entry cell, mark it visited, push it onto a stack
2. Look at the current cell's unvisited neighbours
3. If any exist, pick one randomly, knock down the wall between them, move into it
4. If none exist, backtrack by popping the stack
5. Repeat until every cell has been visited

We chose this algorithm because:
- It is simple to implement and easy to understand and defend
- It naturally produces a perfect maze (spanning tree) with no extra logic
- It tends to create long winding corridors which look visually interesting
- Reproducibility via seed is trivial since it uses Python's `random` module

## Reusable module — mazegen

The maze generation logic is packaged as a standalone pip-installable module.

### Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage
```python
from mazegen import MazeGenerator

# Create and generate a maze
mg = MazeGenerator(width=20, height=15, seed=42)
mg.generate(entry=(0, 0), exit_=(19, 14), perfect=True)

# Access the results
print(mg.grid)      # list[list[int]] — grid[y][x] = bitmask 0-15
print(mg.entry)     # (0, 0)
print(mg.exit_)     # (19, 14)
print(mg.solution)  # "NEESSWW..." shortest path string
```

### Custom parameters
```python
# Non-perfect maze with loops
mg = MazeGenerator(width=30, height=20, seed=99)
mg.generate(entry=(0, 0), exit_=(29, 19), perfect=False)

# No seed — different maze every run
mg = MazeGenerator(width=10, height=10)
mg.generate(entry=(0, 0), exit_=(9, 9))
```

### Building from source
```bash
pip install build
python3 -m build
```

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck](https://weblog.jamisbuck.org/2010/12/27/maze-generation-depth-first-search)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [BFS explanation](https://en.wikipedia.org/wiki/Breadth-first_search)

### AI usage
Claude (claude.ai) was used during this project for:
- Explaining concepts (bitmask encoding, BFS, recursive backtracker algorithm)
- Reviewing code for bugs and correctness
- Helping structure the project layout and file responsibilities

All generated or suggested code was reviewed, understood, and manually
integrated by the team. No code was blindly copied without understanding it.

## Team

- **dael-ter** — Maze engine: data model, generation algorithm, pathfinder,
  42 pattern, reusable package and pip packaging
- **[teammate login]** — Interface: config parser, output writer, ASCII
  display, interactive menu, main entry point, Makefile

### Planning

We split the project into two vertical slices from the start:
Person A owned all maze internals, Person B owned everything that
touches files and the terminal. We agreed on the `MazeGenerator`
interface (attributes and method signatures) before writing any logic,
which let us work in parallel without blocking each other.

### What worked well
- The clean split between engine and interface meant we never blocked each other
- Building `maze.py` first (data model) before any algorithm made everything else easier
- Testing with small mazes (5×5) early caught bugs before they got complex

### What could be improved
- We could have committed more frequently from the start
- Lint errors should have been fixed as we went, not left to the end

### Tools used
- VS Code
- Claude (claude.ai) for explanations and code review
- Python venv for dependency isolation
- Git for version control