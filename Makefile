PYTHON = python3
ENTRY = a_maze_ing.py
CONFIG = config.txt

.PHONY: all run install debug clean lint lint-strict

all: run

run:
	$(PYTHON) $(ENTRY) $(CONFIG)

install:
	pip install -r requirements.txt

debug:
	$(PYTHON) -m pdb $(ENTRY) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	flake8 .
	mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict