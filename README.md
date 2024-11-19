# Sistema Bibliotecário em Python

Autores: Douglas Lobo, Flávio Marques, Kíria Amanájas, Tiago Novo

## Objetivos
Vamos por fases desenvolver essa aplicação para gestão de uma biblioteca:
- [x] Alinhar equipa e decidir os fundamentos
- [ ] Avaliar e atribuir tarefas para todos
- [ ] Implementar funcionalidades para além do sistema bibliotecário
  - [ ] Fila de empréstimo (`queue.py` + `database.py` + `books.py`)
  - [ ] Algoritmo de recomendações (`recommendations.py`)
- [ ] Melhorar a experiência do usuário (interface gráfica com [PyQt](https://doc.qt.io/qtforpython-6/))
- [ ] Sistema de notificações


## Nosso método
- Vamos usar *typing hint* no projeto, conforme o [link](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) para garantir a tipagem estática e maior clareza no código.
- Vamos usar o inglês como base para nomeação das variáveis e funções. A documentação será em português.
- As pastas definem a função dos módulos: 
  - `helpers`: Módulos auxiliares para funções de apoio e utilitários que não são o foco principal da aplicação.
  - `models`: Módulos para manipulação dos modelos de dados, que correspondem às tabelas da base de dados.
- Comentar os processos e fluxos importantes, mas não comentar cada linha de código. O código deve ser claro o suficiente para se entender com facilidade.
  
## Estrutura do Projeto

```
helpers/
    database.py         # Funções auxiliares para manipulação da base de dados
    queue.py            # Funções auxiliares para manipulação de filas
    notifications.py    # Funções para envio de notificações
    recommendations.py  # Funções para gerar recomendações
models/
    audit.py            # Modelo para auditoria de ações
    lendings.py         # Modelo para empréstimos
    users.py            # Modelo para usuários
    books.py            # Modelo para livros
main.py                 # Ponto de entrada do sistema
```

## Explicações

### O que é um modelo
Um modelo é uma abstração de uma tabela da base de dados. Por exemplo, a tabela `books` terá o modelo `Book`. Isso é feito para garantir que as funções interajam com objetos do tipo `Book` e não diretamente com dados puros, como dicionários.

Um **dicionário** não é igual a um objeto `Book`. Por exemplo, o código abaixo pode ser usado para representar um livro, mas o comportamento do objeto `Book` será mais robusto e permitirá o uso de métodos específicos para manipulação de dados.

```python
book = {"titulo": VALOR,
        "data_publicacao": VALOR,
        "sinopse": VALOR,
        "editora": VALOR,
        "generos": VALOR}
```

Entretanto, isso é diferente de:

```python
book = Book(titulo=VALOR, 
            data_publicacao=VALOR, 
            sinopse=VALOR,
            editora=VALOR,
            generos=VALOR)
```

Com isso, podemos garantir uma maior organização e flexibilidade no código.

### O que é um helper
Um módulo helper é utilizado para funções auxiliares que ajudam a evitar repetição de código. Ele centraliza tarefas repetitivas ou específicas que são usadas em múltiplos pontos do sistema.

Exemplo: funções para manipulação de banco de dados, como adicionar, editar ou deletar registros.

### O que é BREAD
O [BREAD](https://github.com/thangchung/clean-architecture-dotnet/wiki/BREAD-vs-CRUD) (Browse, Read, Edit, Add, Delete) representa as operações básicas de manipulação de dados em um sistema. Essas operações devem ser implementadas de forma simples e reutilizável, de modo que possam ser usadas em diferentes pontos da aplicação para interagir com as tabelas de dados.

**BREAD** se refere a:
- **Browse**: Buscar todos os registros de uma tabela.
- **Read**: Ler um registro específico.
- **Edit**: Editar um registro existente.
- **Add**: Adicionar um novo registro.
- **Delete**: Deletar um registro existente.

Essas operações devem ser implementadas de forma genérica e reutilizável, para que possam ser usadas por diferentes modelos, como `User`, `Book`, `Lending`, etc.

### Sistema de Recomendações

O sistema de recomendações é baseado nos empréstimos feitos por um usuário no último ano. O processo é o seguinte:
1. **Iteração sobre os empréstimos**: Vamos analisar todos os empréstimos feitos pelo usuário no último ano e coletar os gêneros dos livros que ele pegou emprestado.

2. **Ranking de gêneros mais solicitados**: A partir dessa coleta, vamos ranquear os gêneros mais solicitados pelo usuário, identificando os dois gêneros mais pedidos.

3. **Escolha do livro de contrapeso**: Para evitar recomendações tendenciosas, o sistema também selecionará o gênero menos solicitado de todos, para que ele sirva como contrapeso na recomendação.

4. **Geração de recomendações**: Com base nos dois gêneros mais solicitados e no gênero menos solicitado, o sistema irá gerar recomendações que equilibram os gostos do usuário com uma variedade de opções.

Esse sistema dará recomendações mais personalizadas, levando em consideração os padrões de leitura do usuário, sugerindo, porém, também algo novo para ampliar os seus horizontes.
