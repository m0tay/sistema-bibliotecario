from dataclasses import dataclass, KW_ONLY
from datetime import datetime
from typing import Optional
from helpers import database as db

# Géneros:
genres_list: list[str] = ['Romance', 'Mistério', 'Fantasia', 'Ficção Científica', 'Aventura', 'História', 'Terror', 'Clássicos', 'Poesia', 'Drama', 'Infantojuvenil', 'Autoajuda', 'Religião',
                          'Filosofia', 'Humor', 'Biografia', 'Autobiografia', 'Suspense', 'Thriller', 'Contos', 'Distopia', 'Utopia', 'Realismo', 'Épico', 'Western', 'Policial', 'Chick-lit', 'Jovem Adulto', 'Guerra', 'Ensaios']


@dataclass
class Book:
    table_name = "books"

    # Campos da tabela
    id: int
    _: KW_ONLY
    title: str
    sub_title: Optional[str]
    authors: str
    published_date: datetime
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

    def genres() -> list[str]:
        """
        Método estático que retorna os todos géneros possíveis `Book`.
        """
        return genres_list

    @classmethod
    def browse(cls) -> Optional[list["Book"]]:
        """
        Retorna todos os livros da tabela `books`.
        """
        rows = db.browse(Book.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True))
        return [Book(**row) for row in rows] if rows else None

    @classmethod
    def read(cls, book_id: int) -> Optional["Book"]:
        """
        Retorna um único livro através do id.
        """
        result = db.read(Book.table_name, db.table_fields(
            cls, return_field_names=True, return_field_id=True), f"id = {book_id}")
        return Book(**result) if result else None

    @classmethod
    def edit(cls, book_id: int, **fields) -> Optional["Book"]:
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
        condition: str = f"id = {book_id}"

        db.validate_fields(cls, fields)

        db.edit(Book.table_name, fields, condition)

    @classmethod
    def add(cls, **fields) -> None:
        """
        Insere um livro à tabela `books`.
        """
        db.validate_fields(cls, fields)

        db.add(Book.table_name, fields)

    @staticmethod
    def delete(book_id: int) -> None:
        """
        Deleta um livro da tabela `books` através do id.
        """
        db.delete(Book.table_name, f"id = {book_id}")
