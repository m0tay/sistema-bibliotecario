import sqlite3
from typing import Optional
from dataclasses import fields as dataclass_fields
from datetime import date

# ─────────────────────────────────────────────────────────────────────
# Nós vamos usar o paradigma BREAD: Browse, Read, Add, Edit e Delete.
# Na dúvida, é interessante conferir esse link: https://github.com/thangchung/clean-architecture-dotnet/wiki/BREAD-vs-CRUD
# `noqa: E501` é um código para indicar ao formatador para não dividir a linha em duas com o word wrap
# ─────────────────────────────────────────────────────────────────────


# Conexão com o banco de dados
# Esta função estabelece a conexão com o arquivo onde a base de dados encontra-se
def connect_to_database() -> sqlite3.Connection:
    """
    Estabelece a conexão com o arquivo onde a base de dados encontra-se.
    Retorna um objeto de conexão SQLite.
    """
    return sqlite3.connect("library.sqlite3")


def create_table(model: type[object]) -> None:
    """
    Cria uma nova tabela no banco de dados, se não existir.

    - `model`: Classe do modelo de dados (ex: `User`).
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Criação da query para a criação da tabela
    fields_str = ", ".join(f"{field[0]} {field[1]}" for field in table_fields(model))  # noqa: E501
    query = f"CREATE TABLE IF NOT EXISTS {model.table_name.lower()} ({fields_str})"  # noqa: E501

    cur.executescript(query)
    conn.commit()
    conn.close()

    # print(f"`{table_name}` tabela criada com êxito!")


def drop_table(model: type[object]) -> None:
    """
    Deleta uma tabela do banco de dados, caso exista.

    - `model`: Classe do modelo de dados (ex: `User`).
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Deletando a tabela se ela existir
    cur.execute(f"DROP TABLE IF EXISTS {model.table_name.lower()}")
    conn.commit()
    conn.close()

    # print(f"`{table_name}` tabela deletada com êxito!"


def table_fields(model: type[object]) -> list[tuple[str, str]]:
    """
    Gera dinamicamente os campos e seus tipos SQL correspondentes com base nos campos da dataclass que foi provida.

    - `model`: Classe do modelo de dados (ex: `User`).

    Retorna uma lista de tuplas, onde cada tupla contém:
    - O nome do campo.
    - O tipo SQL correspondente (ex: "TEXT NOT NULL", "INTEGER NULL").
    """
    # Obter os nomes dos campos da classe passada
    field_names = [f.name for f in dataclass_fields(model)]  # noqa: E501

    # field_names_with_id = [f.name for f in dataclass_fields(
    #     model)]

    # if return_field_names:
    #     return field_names_with_id if return_field_id else field_names

    # Define o mapeamento de tipos de Python para tipos SQL 🌹
    type_mapping = {
        str: "TEXT NOT NULL",
        date: "DATETIME NOT NULL",
        int: "INTEGER NOT NULL",
        float: "REAL NOT NULL",
        bool: "INTEGER NOT NULL",
        Optional[date]: "DATETIME NULL",
        Optional[str]: "TEXT NULL",
        Optional[int]: "INTEGER NULL",
        Optional[float]: "REAL NULL",
        Optional[bool]: "INTEGER NULL",
    }

    # Gera a lista de campoœs e tipos SQL
    table_fields = [
        (field_name, type_mapping[field_type] if field_name != "id" else "INTEGER PRIMARY KEY NOT NULL")  # noqa: E501
        for field_name, field_type in zip(field_names, [f.type for f in dataclass_fields(model)])  # noqa: E501
    ]

    return table_fields


def validate_fields(model: type[object], fields: list[str]) -> None:
    """
    Valida os campos fornecidos em relação aos campos definidos no modelo.

    - `model`: Classe do modelo de dados (ex: `User`).
    - `fields`: Lista de campos para validação.

    Levanta `ValueError` caso algum campo seja inválido.
    """
    valid_fields = {field.name for field in dataclass_fields(model)}
    invalid_fields = set(fields) - valid_fields

    if invalid_fields:
        raise ValueError(f"\nCampos inválidos: {
                         invalid_fields}\nCampos válidos: {valid_fields}")


# ─────────────────────────────────────────────────────────────────────
# Funções BREAD (Browse, Read, Add, Edit, Delete) genéricas para modelos.
# Servem como interfaces entre os modelos Python (ex: "Livro") e suas respectivas
# tabelas no banco de dados (ex: "books").
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


def browse(model: type[object], **conditions: Optional[dict[str, any]]) -> Optional[list[dict]]:
    """
    Retorna todos os registros de uma tabela.

    - `model`: Classe do modelo de dados (ex: `User`).
    - `conditions`: Condições de filtro como pares de chave-valor (ex: `id=1`, `name="Nícolas"`).

    Retorna uma lista de modelo com os valores do registro ou [] caso não exista.
    """
    # Conectar ao banco de dados e instanciar cursor
    conn = connect_to_database()
    cur = conn.cursor()

    # Validar os campos providos
    validate_fields(model, conditions.keys())

    # Preparar dados para a construção da query
    where_clause = " AND ".join(f"{key} = ?" for key in conditions.keys())
    values = tuple(conditions.values())

    # Construção da query
    query = f"SELECT * FROM {model.table_name} WHERE {where_clause}" if conditions else f"SELECT * FROM {model.table_name}"  # noqa: E501

    try:
        cur.execute(query, values)
        rows = cur.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    # Preparando dados para a construação do modelo a ser retornado
    field_names = [field[0] for field in table_fields(model)]
    return [model(**dict(zip(field_names, row))) for row in rows] if rows else []


def read(model: type[object], **conditions: dict[str, any]) -> Optional[dict]:
    """
    Retorna um único registro da tabela baseado nas condições fornecidas.

    - `model`: Classe do modelo de dados (ex: `User`).
    - `conditions`: Condições de filtro como pares de chave-valor (ex: `id=1`, `name="Nícolas"`).

    Retorna um modelo com os valores do registro ou [] caso não exista.
    """
    # Conectar ao banco de dados e instanciar cursor
    conn = connect_to_database()
    cur = conn.cursor()

    # Validar os campos providos
    validate_fields(model, conditions.keys())

    # Preparar dados para a construção da query
    field_str = ", ".join(field_name[0] for field_name in table_fields(model))
    where_clause = " AND ".join(f"{key} = ?" for key in conditions.keys())
    values = tuple(conditions.values())

    # Construção da query
    query = f"SELECT {field_str} FROM {model.table_name} WHERE {where_clause}"

    try:
        cur.execute(query, values)
        row = cur.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    # Preparando dados para a construação do modelo a ser retornado
    field_names = [field[0] for field in table_fields(model)]
    return model(**dict(zip(field_names, row))) if row else []


def edit(model: type[object], id: int, **updates: dict[str, any]) -> type[object]:
    """
    Atualiza os campos de um registro identificado pelo `id` com os valores fornecidos.

    - `model`: Classe do modelo de dados (ex: `User`).
    - `id`: Identificador único do registro a ser atualizado.
    - `updates`: Pares de chave-valor representando os campos a serem atualizados (ex: `name="Novo Nome"`, `age=30`).

    Retorna um modelo com os valores atualizados ou [] caso não exista.
    """
    # Conectar ao banco de dados e instanciar cursor
    conn = connect_to_database()
    cur = conn.cursor()

    # Validar os campos providos
    validate_fields(model, updates.keys())

    # Preparar dados para a construção da query
    set_clause = ", ".join(f"{field} = ?" for field in updates)
    values = tuple(updates.values()) + (id,)

    # Construção da query
    query = f"UPDATE {model.table_name} SET {set_clause} WHERE id = ?"

    try:
        cur.execute(query, values)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    updated_instance = read(model, id=id)
    return updated_instance


def add(model: type[object]) -> type[object]:
    """
    Adiciona um novo registro à tabela com base nos dados fornecidos no modelo.

    - `model`: Instância da classe do modelo de dados (ex: `User`). O modelo deve conter todos os campos necessários para o registro.

    Exemplo de uso:
    `db.add(User(name="Nícolas Alves", email="nicolas@alves.com", age=17, gender="M", register_date="2024-11-20"))`

    Executa a inserção no banco de dados e não retorna o registo criado.
    """
    # Conectar ao banco de dados e instanciar cursor
    conn = connect_to_database()
    cur = conn.cursor()

    # Preparando um dicionário a partir dos campos da dataclass do modelo provido e eliminando o "table_name"
    fields = {k: v for k, v in model.__dict__.items() if k != "table_name"}  # noqa: E501

    # Validar os campos providos
    validate_fields(model, fields.keys())

    # Preparar dados para a construção da query
    placeholders = ", ".join("?" for _ in fields)
    fields_str = ', '.join(fields.keys())
    values = tuple(fields.values())

    # Construção da query
    query = f"INSERT INTO {model.table_name} ({fields_str}) VALUES ({placeholders})"  # noqa: E501

    try:
        cur.execute(query, values)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    return model


def delete(model: type[object], *, id: int) -> None:
    """
    Deleta um registro da tabela baseado no id fornecido.

    - `model`: Modelo que representa a tabela no banco de dados.
    - `id`: Identificador único do registro a ser deletado.

    Exemplo de uso:
    delete(Book, id=1)
    """
    # Conectar ao banco de dados e instanciar cursor
    conn = connect_to_database()
    cur = conn.cursor()

    # Construção da query
    query = f"DELETE FROM {model.table_name} WHERE id = {id}"

    try:
        cur.execute(query)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
