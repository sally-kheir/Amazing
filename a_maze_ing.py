import os
import sys
from utils.config_parser import parse_config
from utils.output_writer import write_output
from display.menu import run_menu

from mazegen import MazeGenerator

DEFAULT_CONFIG_CONTENT = """# Default Configuration File
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,0
PERFECT=true
OUTPUT_FILE=output.hex
SEED=42
"""


def ensure_config_exists(config_path: str) -> None:
    """If the config file doesn't exist, it is automatically recreated."""
    if not os.path.exists(config_path):
        print(
            f" '{config_path}' not found"
            "Automatically rebuilding the file...")
        with open(config_path, "w") as f:
            f.write(DEFAULT_CONFIG_CONTENT)
        print(f"New file '{config_path}' created successfully!\n")


def main() -> None:
    """Main entry point of the application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config_filename = sys.argv[1]

    ensure_config_exists(config_filename)

    try:
        config = parse_config(config_filename)
    except Exception as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        generator = MazeGenerator(
            config["width"],
            config["height"],
            config["seed"])
        generator.generate(config["entry"], config["exit"], config["perfect"])
    except Exception as e:
        print(f"Generation Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        write_output(generator, config["output_file"])
    except Exception as e:
        print(f"Output Writer Error: {e}", file=sys.stderr)
        sys.exit(1)

    run_menu(config, generator)


if __name__ == "__main__":
    main()
