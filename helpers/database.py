import sqlite3
from typing import Optional, Union
from typing import Type
from dataclasses import fields as dataclass_fields
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────
# Nós vamos usar o paradigma BREAD: Browse, Read, Add, Edit e Delete.
# Na dúvida, é interessante conferir esse link: https://github.com/thangchung/clean-architecture-dotnet/wiki/BREAD-vs-CRUD
# `noqa: E501` é um código para indicar ao formatador para não dividir a linha em duas com o word wrap
# ─────────────────────────────────────────────────────────────────────


# Conexão com o banco de dados
# Esta função estabelece a conexão com o arquivo onde a base de dados encontra-se
def connect_to_database() -> sqlite3.Connection | Exception:
    """
    Estabelece a conexão com o arquivo onde a base de dados encontra-se.
    Retorna um objeto de conexão SQLite.
    """
    return sqlite3.connect("library.sqlite3")


def create_table(table_name: str, table_fields: list[tuple]) -> None:
    """
    Cria uma nova tabela no banco de dados, se não existir.

    - `table_name`: Nome da tabela a ser criada.
    - `table_fields`: Lista de tuplas, cada uma contendo o nome e tipo do campo.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Criação da query para a criação da tabela
    fields_str = ", ".join(f"{field[0]} {field[1]}" for field in table_fields)
    query = f"CREATE TABLE IF NOT EXISTS {table_name.lower()} (id INTEGER PRIMARY KEY NOT NULL, {fields_str})"  # noqa: E501

    cur.executescript(query)
    conn.commit()
    conn.close()

    # print(f"`{table_name}` tabela criada com êxito!")


def drop_table(table_name: str) -> None:
    """
    Deleta uma tabela do banco de dados, caso exista.

    - `table_name`: Nome da tabela a ser deletada.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Deletando a tabela se ela existir
    cur.execute(f"DROP TABLE IF EXISTS {table_name.lower()}")
    conn.commit()
    conn.close()

    # print(f"`{table_name}` tabela deletada com êxito!"


def clear_table(table_name: str) -> None:
    """
    Elimina todos os dados de uma tabela.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table_name.lower()}")
    conn.commit()
    conn.close()

    # print(f"`{table_name}` tabela foi limpa com êxito!")


def table_fields(table_class: Type[object], return_field_names=False, return_field_id=False) -> list[tuple[str, str]]:
    """
    Gera dinamicamente os campos e seus tipos SQL correspondentes com base nos campos da dataclass que foi provida.

    - `table_class`: A dataclass que representa a tabela no banco de dados.

    Retorna uma lista de tuplas, onde cada tupla contém:
    - O nome do campo.
    - O tipo SQL correspondente (ex: "TEXT NOT NULL", "INTEGER NULL").
    """
    # Obter os nomes dos campos da classe passada
    field_names = [f.name for f in dataclass_fields(
        table_class) if f.name != "id"]  # Excluindo o 'id'

    field_names_with_id = [f.name for f in dataclass_fields(
        table_class)]

    if return_field_names:
        return field_names_with_id if return_field_id else field_names

    # Define o mapeamento de tipos de Python para tipos SQL 🌹
    type_mapping = {
        str: "TEXT NOT NULL",
        datetime: "DATETIME NOT NULL",
        int: "INTEGER NOT NULL",
        float: "REAL NOT NULL",
        bool: "INTEGER NOT NULL",
        Optional[datetime]: "DATETIME NULL",
        Optional[str]: "TEXT NULL",
        Optional[int]: "INTEGER NULL",
        Optional[float]: "REAL NULL",
        Optional[bool]: "INTEGER NULL",
    }

    # Gera a lista de campos e tipos SQL
    table_fields = [
        (field_name, type_mapping[field_type])
        for field_name, field_type in zip(field_names, [f.type for f in dataclass_fields(table_class) if f.name != "id"])
    ]

    return table_fields


def validate_fields(cls: Type[object], fields):
    valid_fields = [field.name for field in dataclass_fields(
        cls) if field.name != "id"]

    for field in fields:
        if field not in valid_fields:
            raise ValueError(f"Campo inválido: '{
                field}'. Campos válidos: {valid_fields}")


# ─────────────────────────────────────────────────────────────────────
# Funções BREAD (Browse, Read, Add, Edit, Delete) genéricas para modelos.
# Servem como interfaces entre os modelos Python (ex: "Livro") e suas respectivas
# tabelas no banco de dados (ex: "books").
#
# Essas funções realizam operações básicas de banco de dados de forma reutilizável:
# - Browse: Consultar múltiplos registros.
# - Read: Ler um único registro.
# - Add: Adicionar novos registros.
# - Edit: Editar registros existentes.
# - Delete: Deletar registros.
#
# O padrão BREAD facilita a manutenção, pois as operações comuns são centralizadas,
# permitindo uma interação consistente com o banco de dados sem necessidade de
# duplicação de código.
# ─────────────────────────────────────────────────────────────────────

def browse(table_name: str, fields: list[str]) -> Optional[list[dict]]:
    """
    Retorna todos os registros de uma tabela.

    - `table_name`: Nome da tabela no banco de dados.
    - `fields`: Lista de campos a serem retornados.

    Retorna uma lista de dicionários ou `None` caso não haja registros.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Construção da query para selecionar os campos
    fields_str = ", ".join(fields)
    query = f"SELECT {fields_str} FROM {table_name}"

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    # Convertendo as linhas para uma lista de dicionários
    return [dict(zip(fields, row)) for row in rows] if rows else None


def read(table_name: str, fields: list[str], condition: str) -> Optional[dict]:
    """
    Retorna um único registro da tabela baseado na condição fornecida.

    - `table_name`: Nome da tabela no banco de dados.
    - `fields`: Lista de campos a serem retornados.
    - `condition`: Condição de filtro (ex: "id = 1").

    Retorna um dicionário com o registro ou `None` caso não exista.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Construção da query para selecionar os campos e aplicar a condição
    field_str = ", ".join(fields)
    query = f"SELECT {field_str} FROM {table_name} WHERE {condition}"

    cur.execute(query)
    row = cur.fetchone()
    conn.close()

    # Convertendo o registro retornado para um dicionário
    return dict(zip(fields, row)) if row else None


def edit(table_name: str, fields: dict[str, str], condition: str) -> None:
    """
    Edita registros existentes na tabela conforme a condição fornecida.

    - `table_name`: Nome da tabela.
    - `fields`: Lista dos campos a serem atualizados.
    - `values`: Lista de valores para os campos a serem atualizados.
    - `condition`: Condição para selecionar os registros a serem atualizados.

    Exemplo de uso:
    edit("books", {"authors": "Harper Lee", "publisher": "Edipro"}, "id = 1")
    """

    conn = connect_to_database()
    cur = conn.cursor()

    # Construindo a cláusula SET da query de atualização
    set_clause = ", ".join(f"{field} = ?" for field in fields)
    values: list[tuple] = [tuple(value for value in fields.values())]
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

    cur.executemany(query, values)
    conn.commit()
    conn.close()

    # print(f"Registro da tabela {table_name} atualizado com êxito!")


def add(table_name: str, fields: dict[str, str]) -> None:
    """
    Adiciona novos registros à tabela.

    - `table_name`: Nome da tabela.
    - `fields`: Dicionário dos campos a serem inseridos.
    - `values`: Lista de valores correspondentes aos campos.

    Exemplo de uso:
    add("livros", ["titulo", "autor"], [("Título do Livro", "Autor do Livro")])
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Gerando placeholders e query de inserção
    placeholders = ", ".join("?" for _ in fields)
    fields_str = ', '.join(fields)
    values: list[tuple] = [tuple(value for value in fields.values())]

    query = f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders})"

    cur.executemany(query, values)
    conn.commit()
    conn.close()

    # print(f"Registro adicionado com êxito na tabela {table_name}!")


def delete(table_name: str, condition: str) -> None:
    """
    Deleta registros da tabela baseado na condição fornecida.

    - `table_name`: Nome da tabela.
    - `condition`: Condição para excluir os registros (ex: "id = 1").

    Exemplo de uso:
    delete("books", "id = 1")
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Construção da query de exclusão
    query = f"DELETE FROM {table_name} WHERE {condition}"

    cur.execute(query)
    conn.commit()
    conn.close()

    # print(f"Registro da tabela {table_name} deletado com êxito!")
