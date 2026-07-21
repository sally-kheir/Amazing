# utils/config_parser.py
import os
import sys
from typing import Dict, Any, Tuple

def parse_config(filepath: str) -> Dict[str, Any]:
    """Lit et valide le fichier de configuration du labyrinthe.

    Args:
        filepath: Le chemin vers le fichier de configuration.

    Returns:
        Un dictionnaire contenant les paramètres validés.
    """
    if not os.path.exists(filepath):
        print(f"Error: config file '{filepath}' not found", file=sys.stderr)
        sys.exit(1)

    config: Dict[str, str] = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    print(f"Error: invalid line format: '{line}'", file=sys.stderr)
                    sys.exit(1)
                key, val = line.split('=', 1)
                config[key.strip().upper()] = val.strip()
    except IOError:
        print("Error: cannot read config file", file=sys.stderr)
        sys.exit(1)

    # Validation des clés obligatoires
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for m_key in mandatory_keys:
        if m_key not in config:
            print(f"Error: missing required key: {m_key}", file=sys.stderr)
            sys.exit(1)

    # Validation des dimensions
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        if width <= 0 or height <= 0:
            raise ValueError
    except ValueError:
        print("Error: WIDTH and HEIGHT must be positive integers greater than 0", file=sys.stderr)
        sys.exit(1)

    # Validation des coordonnées d'entrée/sortie
    def parse_coords(coord_str: str, key_name: str) -> Tuple[int, int]:
        try:
            parts = coord_str.split(',')
            if len(parts) != 2:
                raise ValueError
            cx, cy = int(parts[0]), int(parts[1])
            if not (0 <= cx < width and 0 <= cy < height):
                print(f"Error: {key_name} coordinates outside maze bounds", file=sys.stderr)
                sys.exit(1)
            return cx, cy
        except ValueError:
            print(f"Error: {key_name} must be in format x,y", file=sys.stderr)
            sys.exit(1)

    entry = parse_coords(config["ENTRY"], "ENTRY")
    exit_ = parse_coords(config["EXIT"], "EXIT")

    if entry == exit_:
        print("Error: ENTRY and EXIT must be different", file=sys.stderr)
        sys.exit(1)

    # Validation du booléen PERFECT
    perfect_val = config["PERFECT"].lower()
    if perfect_val in ["true", "1"]:
        perfect = True
    elif perfect_val in ["false", "0"]:
        perfect = False
    else:
        print("Error: PERFECT must be True or False", file=sys.stderr)
        sys.exit(1)

    # Récupération optionnelle du Seed
    seed = None
    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except ValueError:
            pass

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_,
        "output_file": config["OUTPUT_FILE"],
        "perfect": perfect,
        "seed": seed
    }