import sqlite3
from typing import List, Tuple


# Nós vamos usar o paradigma BREAD: Browse, Read, Add, Edit e Delete.
# Na dúvida, é interessante conferir esse link: https://github.com/thangchung/clean-architecture-dotnet/wiki/BREAD-vs-CRUD


# Conexão com o banco de dados
def connect_to_database() -> sqlite3.Connection:
    """
    Estabelece a conexão com o arquivo onde a base de dados encontra-se.
    """
    return sqlite3.connect("library.sqlite3")


def drop_table(table_name: str):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table_name.lower()}")

    conn.commit()
    conn.close()


def create_table(table_name: str, table_fields: List[tuple]):
    conn = connect_to_database()
    cur = conn.cursor()

    script = f"""CREATE TABLE IF NOT EXISTS {
        table_name.lower()} (id INTEGER PRIMARY KEY NOT NULL, """

    for i, field in enumerate(table_fields):
        script += f"{field[0]} {field[1]}"

        if i < len(table_fields) - 1:
            script += ", "

    script += ")"

    cur.executescript(script)

    conn.commit()
    conn.close()

    print(f"`{table_name}` tabela criada com êxito!")


# Funções BREAD genéricas
def browse(table_name: str, fields: List[str]) -> List[dict]:
    """
    Retorna todos os registros de uma tabela.

    - `table_name`: Nome da tabela no banco de dados.
    - `fields`: Lista de campos a serem retornados.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # "id, titulo, autor", "id, nome, data_registo", etc
    field_str = ", ".join(fields)
    query = f"SELECT {field_str} FROM {table_name}"

    cur.execute(query)
    rows = cur.fetchall()

    # Convertendo cada linha em um dicionário
    results = [dict(zip(fields, row)) for row in rows]
    conn.close()

    return results


def add(table_name: str, fields: List[str], values: List[Tuple]) -> None:
    """
    Adiciona um novo registro na tabela.

    - `table_name`: Nome da tabela.
    - `fields`: Lista dos campos que serão inseridos.
    - `values`: Lista de valores correspondentes aos campos.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    placeholders = ", ".join("?" for _ in fields)  # Ex: "?, ?, ?"
    query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({
        placeholders})"

    cur.executemany(query, values)
    conn.commit()
    conn.close()

    print(f"Registros adicionados com sucesso na tabela {table_name}!")


def edit(table_name: str, fields: List[str], values: List[Tuple], condition: str) -> None:
    """
    Edita registros na tabela de acordo com a condição fornecida.

    - `table_name`: Nome da tabela.
    - `fields`: Lista dos campos a serem editados.
    - `values`: Lista de valores para os campos a serem editados.
    - `condition`: Condição para a atualização, ex: "id = 1".
    """
    conn = connect_to_database()
    cur = conn.cursor()

    set_clause = ", ".join(f"{field} = ?" for field in fields)
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

    cur.execute(query, values)
    conn.commit()
    conn.close()

    print(f"Registros da tabela {table_name} atualizados com sucesso!")


def delete(table_name: str, condition: str) -> None:
    """
    Deleta registros da tabela com base na condição.

    - `table_name`: Nome da tabela.
    - `condition`: Condição para deletar, ex: "id = 1".
    """
    conn = connect_to_database()
    cur = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE {condition}"

    cur.execute(query)
    conn.commit()
    conn.close()

    print(f"Registros da tabela {table_name} deletados com sucesso!")
