from datetime import date
from typing import Callable, Dict, Optional, Any
from os import system, name


# Função para limpar o terminal/console
def clear_cli():
    return system("cls") if name == "nt" else system("clear")

# Função para verificar se um índice está fora de um intervalo
def in_range(index: int, browse_range: Dict[str, int]) -> bool:
    return not (browse_range["start"] <= index < browse_range["end"])

# Função para exibir o menu
def menu(options: Optional[Dict[str, Dict[str, Callable[..., Any]]]] = None):
    # Se `options` for `None`, sai imediatamente
    if options is None:
        print("Exiting...")
        return

    while True:
        try:
            print(f"{' ' + date.today().strftime('%A %d, %B %Y') + ' ':-^40}")
            # Processo para exibir as opções com base na estutura provida no dict
            for key, value in options.items():
                print(f"[{key}] {value['text']}")

            choice = input("Enter your choice: ")
            action = options.get(choice)

            if action and callable(action["func"]):
                clear_cli()
                if action["func"]():
                    break
            else:
                clear_cli()
                print("Invalid choice. Please try again.")
        except (KeyboardInterrupt, EOFError):
            clear_cli()
            print("Use the menu options to exit.")

# Função para criar submenus
def submenu(options: Dict[str, Dict[str, Any]], text: Optional[str] = None) -> Callable:
    def menu_handler() -> bool:
        if text is not None:
            print(text)
        menu(options)
        return False
    return menu_handler
