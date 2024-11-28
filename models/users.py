from dataclasses import dataclass, fields as dataclass_fields, KW_ONLY
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
    email: str
    age: int
    gender: Optional[str]
    register_date: datetime

    def __str__(self):
        return (f"\n\tUser ID: {self.id}\n"
                f"\tName: {self.name}\n"
                f"\tEmail: {self.email}\n"
                f"\tAge: {self.age}\n"
                f"\tGender: {self.gender}\n"
                f"\tRegistered at: {self.register_date}\n")

    @classmethod
    def preferences(cls):
        """
        Retorna em ranque os géneros preferidos dos usuário.
        """
        pass

    @classmethod
    def browse(cls) -> Optional[list["User"]]:
        """
        Retorna todos os usuários da tabela `users`.
        """
        rows = db.browse(User.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True))
        return [User(**row) for row in rows] if rows else None

    @classmethod
    def read(cls, user_id: int) -> Optional["User"]:
        """
        Retorna um único usuário através do id.
        """
        result = db.read(User.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True), f"id = {user_id}")
        return User(**result) if result else None

    @classmethod
    def edit(cls, user_id: int, **fields) -> Optional["User"]:
        """
        Atualiza o registo especificado.

        Campos da tabela
        - `name`
        - `email`
        - `age`
        - `gender`
        - `register_date`
        """
        condition: str = f"id = {user_id}"

        db.validate_fields(cls, fields)

        db.edit(User.table_name, fields, condition)

    @classmethod
    def add(cls, **fields) -> None:
        """
        Insere um usuário à tabela `users`.
        """
        db.validate_fields(cls, fields)

        db.add(User.table_name, fields)

    @staticmethod
    def delete(user_id: int) -> None:
        """
        Deleta um usuário da tabela `users` através do id.
        """
        db.delete(User.table_name, f"id = {user_id}")
