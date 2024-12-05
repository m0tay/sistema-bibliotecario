from dataclasses import KW_ONLY, dataclass
from datetime import date
from typing import Optional


@dataclass
class Book:
    table_name = "books"

    # Campos da tabela
    id: Optional[int] = None
    _: KW_ONLY
    title: str
    sub_title: Optional[str]
    authors: str
    published_date: date
    synopsis: str
    publisher: str
    isbn: Optional[str]
    genres: str
    pages: Optional[int]

    def __str__(self):
        return (f"\n\t{'Book ID:':.<24}{self.id}\n"
                f"\t{'Title:':.<24}{self.title}\n"
                f"\t{'Sub title:':.<24}{self.sub_title}\n"
                f"\t{'Authors:':.<24}{self.authors}\n"
                f"\t{'Published Date:':.<24}{self.published_date}\n"
                f"\t{'Publisher:':.<24}{self.publisher}\n"
                f"\t{'ISBN:':.<24}{self.isbn}\n"
                f"\t{'Genres:':.<24}{self.genres}\n"
                f"\t{'Synopsis:':.<24}{self.synopsis}\n"
                f"\t{'Pages:':.<24}{self.pages}\n")
