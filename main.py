from helpers import database as db
from models.books import Book

if __name__ == "__main__":

    # limpando qualquer tabela
    # db.clear_table(Book.table_name)

    # "dropando" eliminando a tabela
    db.drop_table(Book.table_name)

    # criando uma teabela com base no modelo
    db.create_table(Book.table_name, db.table_fields(Book))

    # adicionando livros a tabela books
    Book.add(title="The Hobbit", authors="J.R.R. Tolkien", published_date="1937-09-21",
             synopsis="A fantasy novel", publisher="George Allen & Unwin", genres="Fantasy", isbn="9789897391019")

    Book.add(title="1984", authors="George Orwell", published_date="1949-06-08", synopsis="A dystopian novel exploring totalitarianism.",
             publisher="Secker & Warburg", genres="Distopia|Ficção Científica|Clássicos", isbn="9789897391019")

    Book.add(title="Pride and Prejudice", authors="Jane Austen", published_date="1813-01-28",
             synopsis="A romantic novel exploring themes of love and social standing.", publisher="T. Egerton, Whitehall", genres="Romance|Clássicos|Drama", isbn="9789897391019")

    # imprimindo uma lista dos livros na tabela books
    print("Livros:\n", "\n\t".join(
        [str(book) for book in Book.browse()]) if Book.browsable() else "não há livros")

    # retorna o livro com base no id referido
    book = Book.read(3)
    print(f"\n\nRead book: {book}")
    
    # atualiza os campos passados do livro referido
    Book.edit(book_id=3, authors="Lee Harper",
              genres="Drama|Suspense", published_date="2024-11-22")

    # retorna o livro com base no id referido
    book = Book.read(3)
    print(f"\n\nRead book: {book}")

    # retorna o livro com base no id referido
    book = Book.read(2)
    print(f"\n\nRead book: {book}")

    # atualiza os campos passados do livro referido
    Book.edit(book_id=2, authors="Leo Tolstoyi", title="War and Peace")


    # retorna o livro com base no id referido
    book = Book.read(2)
    print(f"\n\nRead book: {book}")

    print("\n\n")

    # retorna o livro com base no id referido
    book = Book.read(2)
    
    # deleta o livro referido da tabela
    Book.delete(book_id=book.id)

    print("\n\n")

    # imprimindo uma lista dos livros na tabela books
    print("Livros:\n", "\n\t".join(
        [str(book) for book in Book.browse()]) if Book.browsable() else "não há livros")
