from helpers import database as db


class Book:
    table_name = "books"
    fields = ["titulo", "data_publicacao", "sinopse", "editora", "generos"]

    @staticmethod
    def browse() -> list:
        """
        Retorna todos os livros da tabela `books`.
        """
        return db.browse(Book.table_name, Book.fields)

    @staticmethod
    def read():
        pass

    @staticmethod
    def edit():
        pass

    @staticmethod
    def add(titulo: str, data_publicacao: str, sinopse: str, editora: str, generos: str) -> None:
        """
        Adiciona um novo livro à tabela `books`.
        """
        db.add(Book.table_name, Book.fields, [
            (titulo, data_publicacao, sinopse, editora, generos)])

    @staticmethod
    def delete():
        pass


table_fields = list(
    zip(Book.fields,
        ["TEXT",
         "DATETIME",
         "TEXT",
         "TEXT",
         "TEXT"]))

db.create_table(Book.table_name, table_fields)
