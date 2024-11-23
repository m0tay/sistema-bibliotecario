from datetime import datetime, timedelta

# Lista de livros disponíveis
livros_disponiveis = [
    {"id": 1, "titulo": "Livro A"},
    {"id": 2, "titulo": "Livro B"},
    {"id": 3, "titulo": "Livro C"},
    {"id": 4, "titulo": "Livro D"},
]

# Usuários e seus empréstimos
usuarios = {}

def emprestar_livro(usuario, id_livro):
    if usuario not in usuarios:
        usuarios[usuario] = {"emprestimos": [], "suspenso_ate": None}
    
    # Verificar suspensão
    if usuarios[usuario]["suspenso_ate"] and datetime.now() < usuarios[usuario]["suspenso_ate"]:
        print(f"Usuário {usuario} está suspenso até {usuarios[usuario]['suspenso_ate']}.")
        return
    
    # Verificar limite de empréstimos
    if len(usuarios[usuario]["emprestimos"]) >= 5:
        print("Usuário já tem 5 livros emprestados.")
        return
    
    # Verificar se o livro está disponível
    livro = next((l for l in livros_disponiveis if l["id"] == id_livro), None)
    if not livro:
        print("Livro não está disponível.")
        return
    
    # Registrar empréstimo
    data_devolucao = datetime.now() + timedelta(days=10)
    usuarios[usuario]["emprestimos"].append({"id": id_livro, "data_devolucao": data_devolucao, "extensoes": 0})
    livros_disponiveis.remove(livro)
    print(f"Livro '{livro['titulo']}' emprestado para {usuario} até {data_devolucao}.")

def extender_emprestimo(usuario, id_livro):
    # Verificar se o livro está emprestado pelo usuário
    emprestimo = next((e for e in usuarios[usuario]["emprestimos"] if e["id"] == id_livro), None)
    if not emprestimo:
        print("Este livro não está emprestado pelo usuário.")
        return
    
    # Verificar se pode estender
    if emprestimo["extensoes"] >= 2:
        print("O empréstimo já foi estendido o máximo de vezes.")
        return
    
    emprestimo["data_devolucao"] += timedelta(days=10)
    emprestimo["extensoes"] += 1
    print(f"Empréstimo do livro {id_livro} estendido até {emprestimo['data_devolucao']}.")

def devolver_livro(usuario, id_livro):
    # Verificar se o livro está emprestado pelo usuário
    emprestimo = next((e for e in usuarios[usuario]["emprestimos"] if e["id"] == id_livro), None)
    if not emprestimo:
        print("Este livro não está emprestado pelo usuário.")
        return
    
    # Verificar atraso
    if datetime.now() > emprestimo["data_devolucao"]:
        print("Devolução atrasada! Usuário será suspenso por 5 dias.")
        usuarios[usuario]["suspenso_ate"] = datetime.now() + timedelta(days=5)
    
    # Devolver o livro
    usuarios[usuario]["emprestimos"].remove(emprestimo)
    livros_disponiveis.append({"id": id_livro, "titulo": f"Livro {chr(64 + id_livro)}"})  # Adiciona de volta na lista
    print(f"Livro {id_livro} devolvido com sucesso.")

# Exemplo de uso
emprestar_livro("João", 1)
emprestar_livro("João", 2)
extender_emprestimo("João", 1)
devolver_livro("João", 1)
devolver_livro("João", 2)
