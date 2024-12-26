import sys
import os
import sqlite3
from typing import List, Tuple
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.users import User
from models.books import Book
from models.audit import Audit

# conn = sqlite3.connect("database")
# cursor = conn.cursor()


# def recommend_books(user, database):
#     #filtrar leitura do ano atual
#     read_user = database[(database["user"] == user)]

#     #contar gêneros mais lidos
#     most_read_genres = read_user["genero"].value_counts()

#     if most_read_genres.empty:
#         return "nenhuma leitura registrada pelo usuário esse ano."
    

#     most_read_genre = most_read_genres.idxmax()
#     least_read_genre = most_read_genres.idmin()

def gerar_recomendacoes(usuario: str, ano: int, conn: sqlite3.Connection) -> List[Tuple[str, str]]:
    from models.lendings import Lending 
    cursor = conn.cursor()
    cursor.execute('''
        WITH genero_leituras AS (
            SELECT genero, COUNT(*) AS total_leituras
            FROM leituras
            WHERE usuario = ? AND ano = ?
            GROUP BY genero
        )
        SELECT genero
        FROM genero_leituras
        ORDER BY total_leituras DESC
        LIMIT 1;
    ''', (usuario, ano))
    genero_mais_lido = cursor.fetchone()

    cursor.execute('''
        WITH genero_leituras AS (
            SELECT genero, COUNT(*) AS total_leituras
            FROM leituras
            WHERE usuario = ? AND ano = ?
            GROUP BY genero
        )
        SELECT genero
        FROM genero_leituras
        ORDER BY total_leituras ASC
        LIMIT 1;
    ''', (usuario, ano))
    genero_menos_lido = cursor.fetchone()

    if not genero_mais_lido or not genero_menos_lido:
        return []
    
    genero_mais_lido = genero_mais_lido[0]
    genero_menos_lido = genero_menos_lido[0]

    cursor.execute('''
        SELECT DISTINCT livro, genero
        FROM livros
        WHERE genero = ? AND livro NOT IN (
            SELECT livro
            FROM leituras
            WHERE usuario = ?
        )
        LIMIT 2;
    ''', (genero_mais_lido, usuario))
    recomendacoes_mais_lidos = cursor.fetchall()

    cursor.execute('''
        SELECT DISTINCT livro, genero
        FROM livros
        WHERE genero = ? AND livro NOT IN (
            SELECT livro
            FROM leituras
            WHERE usuario = ?
        )
        LIMIT 1;
    ''', (genero_menos_lido, usuario))
    recomendacoes_menos_lidos = cursor.fetchall()

    recomendacoes = recomendacoes_mais_lidos + recomendacoes_menos_lidos
    return recomendacoes

def main():
    conn = sqlite3.connect("biblioteca.db")

    usuario = "Alice"
    ano = 2024

    recomendacoes = gerar_recomendacoes(usuario, ano, conn)

    if recomendacoes:
        print("Recomendações de livros:")
        for livro, genero in recomendacoes:
            print(f"- {livro} ({genero})")
    else:
        print("Nenhuma recomendação disponível.")

    conn.close()

if __name__ == "__main__":
    main()



