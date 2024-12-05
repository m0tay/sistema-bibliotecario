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
    id:Optional [int] = None
    _: KW_ONLY
    # falta definir

    def __str__(self):
        ...
