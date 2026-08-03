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


def get_theme_preview(theme_name: str) -> str:
    """Renvoie un petit aperçu coloré (carré de couleur) pour chaque thème."""
    style = ascii_view.THEME_STYLES.get(theme_name)
    reset = ascii_view.COLORS["RESET"]

    if not style:
        return ""

    if theme_name == "RAINBOW":
        wall_color = ascii_view.COLORS["RAINBOW_GRADIENT"][0]
    else:
        wall_color = style["wall"]

    return f"{wall_color}  {style['pattern']}  {reset}"


def select_theme_sub_menu() -> int:
    print("\n --- Select Color Theme ---")

    letters = [chr(ord('a') + i) for i in range(len(ascii_view.THEME_CYCLE))]
    theme_mapping = {}

    for idx, theme in enumerate(ascii_view.THEME_CYCLE):
        letter = letters[idx]
        theme_mapping[letter] = idx

        preview = get_theme_preview(theme)
        print(f"  {letter}. {preview} {theme}")

    print("----------------------------")
    sub_choice = input(
        f"Choose a theme ({letters[0]}-{letters[-1]}): ").strip().lower()

    if sub_choice in theme_mapping:
        return theme_mapping[sub_choice]
    else:
        print("Invalid choice, keeping current theme.")
        time.sleep(1)
        return -1


def run_menu(config: Dict[str, Any], generator: Any) -> None:
    """Lance la boucle interactive d'affichage du labyrinthe."""
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
        current_preview = get_theme_preview(current_theme)
        print(f"Current theme: {current_preview} {current_theme}")
        print("1.Re-generate a new maze")
        print("2.Show/Hide path from entry to exit")
        print("3.Change maze colors")
        print("4.Quit")
        choice = input("\nChoice? (1-4): ").strip()

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
            new_index = select_theme_sub_menu()
            if new_index != -1:
                theme_index = new_index
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")
