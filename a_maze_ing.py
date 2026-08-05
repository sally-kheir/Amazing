import sys
from utils.config_parser import parse_config
from utils.output_writer import write_output
from display.menu import run_menu

from mazegen import MazeGenerator


def main() -> None:
    """Main entry point of the application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config_filename = sys.argv[1]

    try:
        config = parse_config(config_filename)
    except Exception as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        generator = MazeGenerator(
            config["width"],
            config["height"],
            config["seed"]
        )
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
