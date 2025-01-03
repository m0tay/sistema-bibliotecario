from datetime import datetime
import os
import shutil as sh
from .database import DATABASE_FILENAME

# ─────────────────────────────────────────────────────────────────────
# Variáveis e configurações para backup
# - BACKUP_TARGET: Arquivo de banco de dados a ser copiado.
# - BACKUP_DIR: Diretório onde os backups serão armazenados.
# ─────────────────────────────────────────────────────────────────────

BACKUP_TARGET: str = DATABASE_FILENAME
BACKUP_DIR: str = "backups"

# ─────────────────────────────────────────────────────────────────────
# Funções de gerenciamento de backups
# - create_backups_folder: Cria a pasta de backups caso não exista.
# - path: Exibe o caminho completo para a pasta de backups.
# - extract_index: Extrai o índice do nome do arquivo de backup.
# - delete_oldest_backup: Deleta o backup mais antigo da pasta de backups.
# - backup: Cria um novo backup do banco de dados.
# - load_backup: Restaura o backup mais recente.
# - setup: Configura a pasta de backups e cria um backup inicial se necessário.
# - list_backups: Exibe os backups existentes com a data de criação.
# ─────────────────────────────────────────────────────────────────────

def create_backups_folder() -> None:
    """
    Cria a pasta de backups se ela não existir.

    Verifica se o diretório de backups (`BACKUP_DIR`) existe. Caso não, a pasta é criada.
    """
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

def path() -> None:
    """
    Exibe o caminho completo para a pasta de backups.

    Utiliza `os.getcwd()` para exibir o diretório atual concatenado com o nome da pasta de backups.
    """
    print(f"{os.getcwd()}/{BACKUP_DIR}/")

def extract_index(backup_str: str) -> int:
    """
    Extrai o índice do nome de um backup.

    - `backup_str`: Nome do arquivo de backup no formato `backup_<index>_<nome_arquivo>`.
    Retorna o índice como um número inteiro.
    """
    return int(backup_str.split("_")[1])

def delete_oldest_backup() -> None:
    """
    Deleta o backup mais antigo.

    Verifica a lista de backups e apaga o arquivo com o menor índice. Caso não haja backups, exibe uma mensagem de aviso.
    """
    backups = os.listdir(BACKUP_DIR)
    if not backups:
        print("There are no backups!")
        return

    oldest_backup = min(backups, key=extract_index)
    os.remove(os.path.join(BACKUP_DIR, oldest_backup))
    print(f"Deleted {oldest_backup} successfully!")

def backup() -> None:
    """
    Cria um novo backup do banco de dados.

    - Verifica se o número de backups já atingiu o limite de 5.
    - Se não, cria um novo backup com um índice incrementado.
    """
    backups = os.listdir(BACKUP_DIR)
    if len(backups) >= 5:
        print("You've reached the limit of 5 backups at a time!")
        return

    new_index = max((int(backup.split("_")[1]) for backup in backups), default=0) + 1
    backup_name = f"backup_{new_index}_{BACKUP_TARGET}"
    sh.copy2(BACKUP_TARGET, os.path.join(BACKUP_DIR, backup_name))
    print(f"Backup created: {backup_name}")

def load_backup() -> None:
    """
    Restaura o backup mais recente.

    Verifica se há backups na pasta e, se houver, restaura o mais recente para o local do banco de dados.
    """
    backups = os.listdir(BACKUP_DIR)
    if not backups:
        print("There are no backups to load!")
        return

    latest_backup = max(backups, key=lambda b: int(b.split("_")[1]))
    sh.copy2(os.path.join(BACKUP_DIR, latest_backup), BACKUP_TARGET)
    print(f"Loaded backup: {latest_backup}")

def setup() -> None:
    """
    Configura a pasta de backups e cria um backup inicial se necessário.
    """
    create_backups_folder()
    if not os.listdir(BACKUP_DIR):
        backup()

def list_backups() -> None:
    """
    Exibe os backups existentes com a data de criação.

    Exibe uma lista de backups com seus índices e a data de criação formatada. Caso não haja backups, não faz nada.
    """
    if not os.listdir(BACKUP_DIR):
        print("There are bo backups!")
        return

    for backup in os.listdir(BACKUP_DIR):
        index = backup.split("_")[1]
        backup_path = os.path.join(BACKUP_DIR, backup)
        creation_time = os.path.getctime(backup_path)
        creation_date = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{index}: backup (created: {creation_date})")
