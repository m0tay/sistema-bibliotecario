import json
import os

# ─────────────────────────────────────────────────────────────────────
# Variáveis e configurações de arquivos
# - SETTINGS_FILE: Caminho para o arquivo de configurações.
# - DEFAULT_SETTINGS: Configurações padrão usadas caso o arquivo não exista.
# ─────────────────────────────────────────────────────────────────────

SETTINGS_FILE = 'settings.json'
DEFAULT_SETTINGS = {'width': 30, 'page_size': 10}

# ─────────────────────────────────────────────────────────────────────
# Funções de gerenciamento de configurações
# - setup: Inicializa as configurações do sistema a partir de um arquivo.
# - update: Atualiza as configurações existentes e as salva no arquivo.
# ─────────────────────────────────────────────────────────────────────


def setup() -> dict:
    """
    Inicializa as configurações do sistema.

    - Verifica se o arquivo de configurações (`SETTINGS_FILE`) existe.
    - Se não existir, cria o arquivo com `DEFAULT_SETTINGS` e retorna as configurações padrão.
    - Se existir, carrega e retorna as configurações do arquivo.
    """
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(DEFAULT_SETTINGS, file)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE) as file:
        settings = json.load(file)
    return settings


def update(new_settings: dict) -> dict:
    """
    Atualiza as configurações existentes.

    - `new_settings`: Dicionário contendo as novas configurações a serem aplicadas.
    - Carrega as configurações atuais com `setup()`, atualiza com `new_settings`, e salva as novas configurações no arquivo.
    Retorna as configurações atualizadas.
    """
    settings = setup()
    settings.update(new_settings)

    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)

    return settings
