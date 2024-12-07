from dataclasses import KW_ONLY, dataclass, field
from datetime import date
from typing import Optional


@dataclass
class User:
    table_name = "users"

    # Campos da tabela
    id: Optional[int] = None
    _: KW_ONLY
    name: str
    email: str
    age: int
    gender: Optional[str]
    register_date: date

    def __str__(self):
        return (f"\n\t{'User ID:':.<24}{self.id}\n"
                f"\t{'Name:':.<24}{self.name}\n"
                f"\t{'Email:':.<24}{self.email}\n"
                f"\t{'Age:':.<24}{self.age}\n"
                f"\t{'Gender:':.<24}{self.gender}\n"
                f"\t{'Registered at:':.<24}{self.register_date}\n")
