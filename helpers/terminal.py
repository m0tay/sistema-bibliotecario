from datetime import date
from os import name, system
from typing import Dict

# ─────────────────────────────────────────────────────────────────────
# Variáveis e configurações globais
# - SETTINGS: Dicionário global de configurações usado para armazenar as preferências de exibição.
# ─────────────────────────────────────────────────────────────────────

SETTINGS: Dict

# ─────────────────────────────────────────────────────────────────────
# Funções utilitárias
# - setup: Configura as definições globais de exibição.
# - clear_cli: Limpa o terminal dependendo do sistema operacional.
# - in_range: Verifica se um índice está dentro de um intervalo específico.
# - menu: Exibe um menu de opções formatado.
# ─────────────────────────────────────────────────────────────────────


def setup(settings: dict) -> None:
    """
    Configura as definições globais de exibição.

    - `settings`: Dicionário contendo as configurações para exibição, como largura da tela e tamanho da página.
    """
    global SETTINGS
    SETTINGS = settings


def clear_cli() -> int:
    """
    Limpa o terminal ou prompt de comando.

    Utiliza `cls` para Windows e `clear` para outros sistemas operacionais.
    Retorna o código de saída do comando executado.
    """
    return system('cls') if name == 'nt' else system('clear')


def in_range(index: int, browse_range: Dict[str, int]) -> bool:
    """
    Verifica se o índice está dentro de um intervalo definido.

    - `index`: Índice a ser verificado.
    - `browse_range`: Dicionário contendo 'start' e 'end' definindo o intervalo.
    Retorna `True` se o índice estiver dentro do intervalo, caso contrário, `False`.
    """
    return browse_range['start'] <= index < browse_range['end']


def menu(options: Dict[str, str], pages=None) -> None:
    """
    Exibe um menu de opções formatado.

    - `options`: Dicionário de opções para exibição no menu.
    - `pages`: (Opcional) Dicionário contendo informações de paginação, como a página atual e o total de páginas.
    Formata e exibe o menu com base nas configurações globais de exibição (`SETTINGS`).
    """
    global SETTINGS
    if pages:
        print(
            f"{' ' + f'Page: {pages['at']}/{pages['total']} ({SETTINGS['page_size']} per page)' + ' ':-^{SETTINGS['width']}}"
        )
    print(f"{' ' + date.today().strftime('%A %d, %B %Y') + ' ':-^{SETTINGS['width']}}")

    for key, value in options.items():
        print(f'[{key}] {value}')
