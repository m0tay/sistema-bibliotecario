from dataclasses import dataclass, fields as dataclass_fields, KW_ONLY, field
from datetime import datetime
from typing import Optional
from helpers import database as db


@dataclass
class User:
    table_name = "users"

    # Campos da tabela
    id: int
    _: KW_ONLY
    name: str
    register_date: datetime

    def __str__(self):
        return (f"\n\tBook ID: {self.id}\n"
                f"\tNmae: {self.name}\n"
                f"\tRegistered at: {self.register_date}\n")

    @classmethod
    def browse(cls) -> Optional[list["User"]]:
        """
        Retorna todos os livros da tabela `books`.
        """
        rows = db.browse(User.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True))
        return [User(**row) for row in rows] if rows else None

    @classmethod
    def read(cls, user_id: int) -> Optional["User"]:
        """
        Retorna um único livro através do id.
        """
        result = db.read(User.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True), f"id = {user_id}")
        return User(**result) if result else None

    @staticmethod
    def edit(user_id: int, **fields) -> Optional["User"]:
        """
        Atualiza o registo especificado.

        Campos da tabela
        - `title`: Armazena o título da obra.
        - `authors`: Lista de autores da obra.
        - `published_date`: Data de publicação da obra.
        - `synopsis`: Resumo ou descrição da obra.
        - `publisher`: Editora responsável pela publicação.
        - `genres`: Gêneros aos quais a obra pertence.
        """

        condition: str = f"id = {user_id}"

        db.edit(User.table_name, fields, condition)

    @classmethod
    def add(cls, **fields) -> None:
        """
        Insere um usuário à tabela `users`.
        """
        valid_fields = [field.name for field in dataclass_fields(
            User) if field.name != "id"]

        for field in fields:
            if field not in valid_fields:
                raise ValueError(f"Campo inválido: '{
                                 field}'. Campos válidos: {valid_fields}")

        values = [(value for value in fields.values())]
        db.add(User.table_name, fields)

    @staticmethod
    def delete(user_id: int) -> None:
        """
        Deleta um livro da tabela `books` através do id.
        """
        db.delete(User.table_name, f"id = {user_id}")
