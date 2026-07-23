# a_maze_ing.py
import sys
from utils.config_parser import parse_config
from utils.output_writer import write_output
from display.menu import run_menu

# Importation du package réutilisable développé par Danah
from mazegen import MazeGenerator


def main() -> None:
    """Point d'entrée principal de l'application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    # 1. Parsing et validation stricte de la configuration
    config = parse_config(sys.argv[1])

    # 2. Instanciation et appel du moteur algorithmique (Danah)
    try:
        generator = MazeGenerator(
            config["width"],
            config["height"],
            config["seed"])
        generator.generate(config["entry"], config["exit"], config["perfect"])
    except Exception as e:
        print(f"Generation Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Écriture immédiate du fichier de sortie au format Hexa
    write_output(generator, config["output_file"])

    # 4. Lancement de la boucle utilisateur d'affichage
    run_menu(config, generator)


if __name__ == "__main__":
    main()
