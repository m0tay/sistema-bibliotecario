from dataclasses import KW_ONLY, dataclass
from datetime import datetime
from typing import Optional

from helpers import database as db
from models.books import Book
from models.users import User


@dataclass
class Lending:
    table_name = "lendings"

    # Campos da tabela
    id: int
    _: KW_ONLY
    user_id: int
    book_id: int
    from_date: datetime
    to_date: datetime

    def __str__(self):
        return (f"\n{'Lending ID:':.<32}{self.id}\n"
                f"\t{'User:'}{User.read(self.user_id)}\n"
                f"\t{'Book'}{Book.read(self.book_id)}\n"
                f"\t{'From date:':.<24}{self.from_date}\n"
                f"\t{'To date:':.<24}{self.to_date}\n")

    @classmethod
    def from_user(cls, user_id: int) -> Optional[list["Lending"]]:
        """
        Retorna todos os empréstimos da tabela `lendings` a partir do id do usuário atrelados a estes.
        """
        condition: str = f"id = {user_id}"

        rows = db.browse(cls.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True), condition)

        return [cls(**row) for row in rows] if rows else None

    @classmethod
    def browse(cls) -> Optional[list["Lending"]]:
        """
        Retorna todos os empréstimos da tabela `lendings`.
        """
        rows = db.browse(cls.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True))
        return [cls(**row) for row in rows] if rows else None

    @classmethod
    def read(cls, lending_id: int) -> Optional["Lending"]:
        """
        Retorna um único empréstimo através do id.
        """
        result = db.read(cls.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True), f"id = {lending_id}")
        return cls(**result) if result else None

    @classmethod
    def edit(cls, lending_id: int, **fields) -> Optional["Lending"]:
        """
        Atualiza o registo especificado.

        Campos da tabela
        - `user_id`
        - `book_id`
        - `from_date`
        - `to_date`
        """
        condition: str = f"id = {lending_id}"

        db.validate_fields(cls, fields)

        db.edit(Lending.table_name, fields, condition)

    @classmethod
    def add(cls, **fields) -> None:
        """
        Insere um empréstimo à tabela `lendings`.
        """
        db.validate_fields(cls, fields)

        db.add(Lending.table_name, fields)

    @staticmethod
    def delete(lending_id: int) -> None:
        """
        Deleta um empréstimo da tabela `lendings` através do id.
        """
        db.delete(Lending.table_name, f"id = {lending_id}")
