# utils/config_parser.py
import os
from typing import Dict, Any, Tuple


def _parse_coords(val: str, key_name: str) -> Tuple[int, int]:
    """Extrait et valide une paire de coordonnées (x, y)."""
    parts = val.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key_name} doit être au format X,Y (ex: 0,0)")
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
        if x < 0 or y < 0:
            raise ValueError(f"{key_name} ne peut pas contenir de valeurs négatives")
        return x, y
    except ValueError:
        raise ValueError(f"{key_name} doit contenir des entiers valides")


def parse_config(filepath: str) -> Dict[str, Any]:
    """Parse le fichier de configuration en gérant les doublons et commentaires."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier de configuration introuvable: {filepath}")

    raw_config: Dict[str, str] = {}

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            # 1. Retirer les espaces aux extrémités
            line = line.strip()

            # 2. Ignorer les lignes vides ou qui commencent par un commentaire '#'
            if not line or line.startswith("#"):
                continue

            # 3. Retirer les commentaires inline (en fin de ligne après '#')
            if "#" in line:
                line = line.split("#", 1)[0].strip()

            # S'il ne reste rien après avoir retiré le commentaire inline
            if not line:
                continue

            # 4. Vérifier la structure CLE=VALEUR
            if "=" not in line:
                raise ValueError(f"Ligne {line_num} invalide (attendu CLE=VALEUR): '{line}'")

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            # 5. DÉTECTION DES DOUBLONS : Refuser si la clé existe déjà
            if key in raw_config:
                raise ValueError(f"Clé dupliquée détectée à la ligne {line_num}: '{key}'")

            raw_config[key] = value

    # 6. Vérification des clés obligatoires
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"}
    missing_keys = required_keys - set(raw_config.keys())
    if missing_keys:
        raise ValueError(f"Clés obligatoires manquantes dans la config: {', '.join(missing_keys)}")

    # 7. Parsing et conversion des valeurs
    try:
        width = int(raw_config["WIDTH"])
        height = int(raw_config["HEIGHT"])
        if width <= 0 or height <= 0:
            raise ValueError("WIDTH et HEIGHT doivent être supérieurs à 0")
    except ValueError:
        raise ValueError("WIDTH et HEIGHT doivent être des entiers valides")

    entry = _parse_coords(raw_config["ENTRY"], "ENTRY")
    exit_ = _parse_coords(raw_config["EXIT"], "EXIT")

    # Validation du type booléen
    perfect_str = raw_config["PERFECT"].lower()
    if perfect_str in ("true", "1", "yes"):
        perfect = True
    elif perfect_str in ("false", "0", "no"):
        perfect = False
    else:
        raise ValueError("PERFECT doit être un booléen (true/false)")

    # Gestion de SEED (optionnel)
    seed = None
    if "SEED" in raw_config:
        try:
            seed = int(raw_config["SEED"])
        except ValueError:
            raise ValueError("SEED doit être un entier valide")

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_,
        "perfect": perfect,
        "output_file": raw_config["OUTPUT_FILE"],
        "seed": seed,
    }