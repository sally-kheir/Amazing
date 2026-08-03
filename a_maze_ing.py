# a_maze_ing.py
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
    """Si le fichier de config n'existe pas, on le recrée automatiquement."""
    if not os.path.exists(config_path):
        print(
            f"⚠️  '{config_path}' introuvable."
            "Reconstitution automatique du fichier...")
        with open(config_path, "w") as f:
            f.write(DEFAULT_CONFIG_CONTENT)
        print(f"✅ Nouveau fichier '{config_path}' créé avec succès !\n")


def main() -> None:
    """Point d'entrée principal de l'application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config_filename = sys.argv[1]

    # 1. Vérifie si le fichier existe, sinon le récrée automatiquement
    ensure_config_exists(config_filename)

    # 2. Parsing et validation de la configuration
    try:
        config = parse_config(config_filename)
    except Exception as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Instanciation et appel du moteur algorithmique
    try:
        generator = MazeGenerator(
            config["width"],
            config["height"],
            config["seed"])
        generator.generate(config["entry"], config["exit"], config["perfect"])
    except Exception as e:
        print(f"Generation Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Écriture immédiate du fichier de sortie au format Hexa
    try:
        write_output(generator, config["output_file"])
    except Exception as e:
        print(f"Output Writer Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Lancement de la boucle utilisateur d'affichage
    run_menu(config, generator)


if __name__ == "__main__":
    main()
