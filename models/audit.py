from dataclasses import KW_ONLY, dataclass
from datetime import datetime
from typing import Optional

from helpers import database as db
from models.books import Book
from models.users import User


@dataclass
class Audit:
    table_name = "audits"

    # Campos da tabela
    id: int
    _: KW_ONLY
    # falta definir

    def __str__(self):
        ...

    @classmethod
    def browse(cls) -> Optional[list["Audit"]]:
        """
        Retorna todos os registros da tabela `audits`.
        """
        pass

    @classmethod
    def read(cls, audit_id: int) -> Optional["Audit"]:
        """
        Retorna um único registro de auditoria através do id.
        """
        pass

    @classmethod
    def edit(cls, audit_id: int, **fields) -> Optional["Audit"]:
        """
        Atualiza o registro especificado.

        Campos da tabela
        `falta definir`
        """
        pass

    @classmethod
    def add(cls, **fields) -> None:
        """
        Insere um novo registro de auditoria na tabela `audits`.
        """
        pass

    @staticmethod
    def delete(audit_id: int) -> None:
        """
        Deleta um registro de auditoria da tabela `audits` através do id.
        """
        pass