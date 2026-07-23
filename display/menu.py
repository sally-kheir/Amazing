# display/menu.py
import os
import time
from typing import Any, Dict

from display import ascii_view

# Delai (en secondes) entre chaque case reveleee de l'animation du chemin
PATH_ANIMATION_DELAY = 0.05


def clear_screen() -> None:
    """Efface le terminal (compatible Windows et Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def animate_path_reveal(generator: Any, theme_name: str) -> None:
    """Affiche le chemin case par case, doucement, au lieu de tout d'un coup."""
    ordered_path = ascii_view.build_path_cells(generator)
    if not ordered_path:
        clear_screen()
        print(
            ascii_view.render(
                generator,
                show_path=False,
                theme_name=theme_name))
        print("\nNo path available to display.")
        return

    for revealed in range(1, len(ordered_path) + 1):
        clear_screen()
        print(ascii_view.render(
            generator,
            show_path=True,
            theme_name=theme_name,
            path_reveal_count=revealed,
        ))
        time.sleep(PATH_ANIMATION_DELAY)


def run_menu(config: Dict[str, Any], generator: Any) -> None:
    """Lance la boucle interactive d'affichage du labyrinthe.

    Args:
        config: dictionnaire de configuration deja valide.
        generator: instance de MazeGenerator deja generee.
    """
    show_path = False
    theme_index = 0

    while True:
        current_theme = ascii_view.THEME_CYCLE[theme_index]

        if show_path:
            animate_path_reveal(generator, current_theme)
        else:
            clear_screen()
            print(
                ascii_view.render(
                    generator,
                    show_path=False,
                    theme_name=current_theme))

        print("\n=== A-Maze-ing ===")
        print(f"Current theme: {current_theme}")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors (Strawberry -> Lilac -> Rainbow -> 42)")
        print("4. Quit")
        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            try:
                generator.generate(
                    config["entry"],
                    config["exit"],
                    config["perfect"])
            except Exception as e:
                print(f"Generation Error: {e}")
                input("Press Enter to continue...")
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(ascii_view.THEME_CYCLE)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")
