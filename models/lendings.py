from dataclasses import KW_ONLY, dataclass
from datetime import date
from typing import Optional

from helpers import database as db
from models.books import Book
from models.users import User


@dataclass
class Lending:
    table_name = "lendings"

    # Campos da tabela
    id: Optional[int] = None
    _: KW_ONLY
    user_id: int
    book_id: int
    from_date: date
    to_date: date

    def __str__(self):
        return (f"\n{'Lending ID:':.<32}{self.id}\n"
                f"\t{'User:':.<24}{db.read(User, id=self.user_id)}\n"
                f"\t{'Book:':.<24}{db.read(Book, id=self.book_id)}\n"
                f"\t{'From date:':.<24}{self.from_date}\n"
                f"\t{'To date:':.<24}{self.to_date}\n")
