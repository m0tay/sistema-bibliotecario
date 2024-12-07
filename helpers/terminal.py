from datetime import date
from typing import Optional
from datetime import date
from os import name, system
from typing import Optional
from time import sleep


def clear_cli():
    return system("cls") if name == "nt" else system("clear")


def in_range(index: int, browse_range: dict[str, int]) -> bool:
    return not (browse_range["start"] <= index < browse_range["end"])


def menu(options: Optional[dict[str, dict[str, callable]]] = None):
    # Verifica se `options` foi passado; se não, cria um menu básico com a opção de sair
    if not options:
        def exit_menu() -> bool:
            print("Exiting...")
            return True

        options = {"0": {"text": "Exit", "func": exit_menu}}

    while True:
        try:
            print(f"{' ' + date.today().strftime('%A %d, %B %Y') + ' ':-^40}")

            # Itera sobre a lista de valores no menu atual
            for key, value in options.items():
                print(f"[{key}] {value['text']}")

            choice = input("Enter your choice: ")
            # Associa escolha do usuário a uma opção dentre as opções
            action = options.get(choice)

            # Verifica se a opção é válida e se tem uma função junto
            if action and callable(action["func"]):
                clear_cli()
                # Executa a função e se ela retornar True quebra o while loop
                if action["func"]():
                    break
            else:
                clear_cli()
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            # Previne o usuário de fechar acidentalmente o programa
            clear_cli()
            print("Use the menu options to exit.")
        except EOFError:
            # Previne o usuário de fechar acidentalmente o programa
            clear_cli()
            print("Use the menu options to exit.")


def submenu(options: dict[str, callable]) -> callable:
    # Retorna uma função (handler) que gerencia o submenu
    def menu_handler() -> bool:
        # Exibe o título do submenu e executa o menu com as opções do submenu
        # print(f"{" " + parent_menu + " sub menu ":-^30}")
        menu(options)
        # Retorna False para voltar ao menu principal ao encerrar o submenu
        return False
    return menu_handler
