from dataclasses import dataclass, fields as dataclass_fields, KW_ONLY, field
from datetime import datetime
from typing import Optional, TypedDict
from helpers import database as db
from warnings import deprecated

# Géneros:
genres_list: list[str] = ['Romance', 'Mistério', 'Fantasia', 'Ficção Científica', 'Aventura', 'História', 'Terror', 'Clássicos', 'Poesia', 'Drama', 'Infantojuvenil', 'Autoajuda', 'Religião',
                          'Filosofia', 'Humor', 'Biografia', 'Autobiografia', 'Suspense', 'Thriller', 'Contos', 'Distopia', 'Utopia', 'Realismo', 'Épico', 'Western', 'Policial', 'Chick-lit', 'Jovem Adulto', 'Guerra', 'Ensaios']


# Fiz isso, mas acho que vou remover futuramente, basicamente o intuito era dar um typing hint na hora de preencher os campos no Book.add(), mas ou o pylance não consegue fazer algo tão complexo ou eu sou idiota

class BookFields(TypedDict):
    title: str
    authors: str
    published_date: datetime
    synopsis: str
    publisher: str
    isbn: str
    genres: str


@dataclass
class Book:
    table_name = "books"

    # Campos da tabela
    id: int
    _: KW_ONLY
    title: str
    authors: str
    published_date: datetime
    synopsis: str
    publisher: str
    isbn: str
    genres: str

    # @classmethod
    # def fields(cls, include_id=False) -> list[str]:
    #     """
    #     Método estático que retorna os nomes dos campos do dataclass `Book`.
    #     """

    #     if include_id:
    #         return db.table_fields(cls, return_field_names=True, return_field_id=True)

    #     # Excluindo o campo "id"
    #     return db.table_fields(cls, return_field_names=True)

    # NÃO APAGAR: Versão antiga para referência
    # @staticmethod
    # def fields(include_id=False) -> list[str]:
    #     """
    #     Método estático que retorna os nomes dos campos do dataclass `Book`.
    #     """

    #     if include_id:
    #         return [f.name for f in dataclass_fields(Book)]

    #     # Excluindo o campo "id"
    #     return [f.name for f in dataclass_fields(Book) if f.name != "id"]

    def __str__(self):
        return (f"\n\tBook ID: {self.id}\n"
                f"\tTitle: {self.title}\n"
                f"\tAuthors: {self.authors}\n"
                f"\tPublished Date: {self.published_date}\n"
                f"\tPublisher: {self.publisher}\n"
                f"\tISBN: {self.isbn}\n"
                f"\tGenres: {self.genres}\n"
                f"\tSynopsis: {self.synopsis}")

    def genres() -> list[str]:
        """
        Método estático que retorna os todos géneros possíveis `Book`.
        """
        return genres_list

    @classmethod
    def browsable(cls) -> bool:
        """
        Retorna todos os livros da tabela `books`.
        """
        rows = db.browse(Book.table_name, db.table_fields(
            cls, return_field_names=True))
        return True if rows else False

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

        # NÃO APAGAR: Versão antiga para referência
        # @staticmethod
        # def read(search_param: Optional[Union[int, str]]) -> Optional["Book"]:
        #     """
        #     Retorna um único livro através do id ou outros campos.
        #     """
        #     for field in Book.fields():
        #         try:
        #             if isinstance(search_param, str) and search_param:
        #                 condition = f"{field} LIKE '%{search_param}%'"
        #             elif isinstance(search_param, int):
        #                 condition = f"id = {search_param}"
        #             else:
        #                 continue  # Skip invalid conditions

        #             result = db.read(
        #                 Book.table_name, Book.fields(include_id=True), condition)
        #             if result:
        #                 return Book(**result)
        #         except Exception as e:
        #             print(f"Error reading book: {e}")
        #             return None

        # result = db.read(Book.table_name, Book.fields() +
        #  ["id"], f"id = {book_id}")
        # return Book(**result) if result else None

    @staticmethod
    def edit(book_id: int, **fields: "BookFields") -> Optional["Book"]:
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

        db.edit(Book.table_name, fields, condition)

        # NÃO APAGAR: Versão antiga para referência
        # @staticmethod
        # def edit(book_id: int, title: Optional[str], authors: Optional[str], published_date: Optional[datetime], synopsis: Optional[str], publisher: Optional[str], genres: Optional[str]) -> Optional["Book"]:
        #     """
        #     Atualiza o registo especificado.
        #     """

        #     values: list[tuple]
        #     condition: str = f"id = {book_id}"
        #     db.edit(Book.table_name, Book.fields(include_id=False), values, condition)

    @classmethod
    def add(cls, **fields: "BookFields") -> None:
        """
        Insere um livro à tabela `books`.
        """
        valid_fields = [field.name for field in dataclass_fields(
            Book) if field.name != "id"]

        for field in fields:
            if field not in valid_fields:
                raise ValueError(f"Campo inválido: '{
                                 field}'. Campos válidos: {valid_fields}")

        values = [(value for value in fields.values())]
        db.add(Book.table_name, fields)

        # NÃO APAGAR: Versão antiga para referência
        # @staticmethod
        # def add(title: str, authors: str, published_date: datetime, synopsis: str, publisher: str, genres: str) -> None:
        #     """
        #     Insere um livro à tabela `books`.
        #     """
        #     values = [(title, authors, published_date,
        #                synopsis, publisher, genres)]
        #     db.add(Book.table_name, Book.fields(include_id=False), values)

    @staticmethod
    def delete(book_id: int) -> None:
        """
        Deleta um livro da tabela `books` através do id.
        """
        db.delete(Book.table_name, f"id = {book_id}")
