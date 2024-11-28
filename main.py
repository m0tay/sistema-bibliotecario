from helpers import database as db
from models.books import Book
from models.users import User
\
if __name__ == "__main__":

    # limpando qualquer tabela
    # db.clear_table(Book.table_name)
    # db.clear_table(User.table_name)

    # "dropando" eliminando a tabela
    db.drop_table(Book.table_name)

    # criando uma teabela com base no modelo
    db.create_table(Book.table_name, db.table_fields(Book))

    # adicionando livros a tabela books
    Book.add(title="The Hobbit", authors="J.R.R. Tolkien", published_date="1937-09-21",
             synopsis="A fantasy novel", publisher="George Allen & Unwin", genres="Fantasy", isbn="9789897391019", pages=410)

    Book.add(title="1984", authors="George Orwell", published_date="1949-06-08", synopsis="A dystopian novel exploring totalitarianism.",
             publisher="Secker & Warburg", genres="Distopia|Ficção Científica|Clássicos", sub_title="the future is now")

    Book.add(title="Pride and Prejudice", authors="Jane Austen", published_date="1813-01-28",
             synopsis="A romantic novel exploring themes of love and social standing.", publisher="T. Egerton, Whitehall", genres="Romance|Clássicos|Drama", isbn="9789897391019", pages=623, sub_title="a novel of two lovers")

    # imprimindo uma lista dos livros na tabela books
    if books := Book.browse():
        print("Livros:\n", "\n\t".join(
            [str(book) for book in books]))
    else:
        print("não há livros")

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
    if books := Book.browse():
        print("Livros:\n", "\n\t".join(
            [str(book) for book in books]))
    else:
        print("não há livros")

    # Interface ao banco de dados
    db.drop_table(User.table_name)
    db.create_table(User.table_name, db.table_fields(User))

    # Interface ao modelo
    User.add(name="Nícolas Alvez", register_date="2024-11-22",
             email="nicolas.alvez@gmail.com", age=17, gender="m")
    User.add(name="Tiago Novo", register_date="2024-11-20",
             email="tiago.novo@gmail.com", age=20, gender="m")
    User.add(name="Eddie", register_date="2024-08-03",
             email="eddie.eddie@gmail.com", age=25)

    if users := User.browse():
        print("Usuários:\n", "\n\t".join(
            [str(user) for user in users]))
    else:
        print("não há usuários")
