# Sistema Bibliotecário em Python

Autores: Douglas Lobo, Flávio Marques, Kíria Amanájas, Tiago Novo

---

## Tabela de Conteúdos

1. Objetivos
2. Nosso Método
3. Estrutura do Projeto
4. Explicações
   1. O que é um Modelo
      1. Diferença entre User.add(), db.add() e add()
   2. O que é um Helper
   3. O que é BREAD
   4. O que é um Decorador
5. Sistema de Recomendações
6. Extensões Recomendadas
7. Como Começar a Trabalhar com o Projeto

---

## Objetivos

Vamos por fases desenvolver essa aplicação para gestão de uma biblioteca:

- [x] Alinhar equipa e decidir os fundamentos
- [x] Avaliar e atribuir tarefas para todos
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

```file
sistema-bibliotecario/
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
book = {title="1984", 
        publication_date="1949-09-31", 
        synopsis="A dystopian future.",
        publisher="Edipro",
        genres="Drama|Suspense|Ficção Científica"}
```

Entretanto, isso é diferente de:

```python
book = Book(title="1984", 
        publication_date="1949-09-31", 
        synopsis="A dystopian future.",
        publisher="Edipro",
        genres="Drama|Suspense|Ficção Científica")
```

Com isso, podemos garantir uma maior organização e flexibilidade no código.

#### Diferença entre `User.add()`, `db.add()` e `add()`

A diferenciação entre essas funções torna o código mais modular, reutilizável e fácil de manter. Cada função tem uma responsabilidade bem definida, o que permite que mudanças sejam feitas em uma camada sem afetar as demais.

1. **`User.add()` (main.py)**: É o ponto de entrada para adicionar um novo usuário no sistema. Ele interage diretamente com a lógica de negócio, como a validação de dados de entrada ou a execução de ações específicas antes de adicionar o usuário. Esse método é específico para o contexto do modelo `User`.

2. **`db.add()` (users.py)**: A função `db.add()` encapsula a lógica de inserção no banco de dados. Ela abstrai os detalhes de execução de SQL e permite que o código seja mais limpo e menos propenso a erros. Aqui, o banco de dados é tratado de forma genérica, podendo ser usado por diferentes modelos, não apenas `User`.

3. **`add()` (database.py)**: Esta função está no módulo auxiliar (helper) e é responsável por construir e executar as queries SQL para inserção. Ela centraliza e padroniza a lógica de inserção de dados, evitando repetição de código e facilitando a manutenção e o entendimento do processo de inserção no banco.

#### Por que isso é melhor?

Essa abordagem modular e segmentada oferece várias vantagens:

- **Separation of concerns (Separação de responsabilidades)**: Cada função tem uma única responsabilidade (adicionar dados no banco, validar dados, gerar queries SQL), o que facilita manutenção e expansão.
  
- **Reusabilidade e Flexibilidade**: A função `db.add()` pode ser reutilizada para diferentes tipos de dados (não só para usuários), sem que a lógica de inserção precise ser reescrita a cada vez. `add()` em `database.py` oferece uma solução genérica que pode ser aplicada em qualquer modelo de dados.

- **Manutenção Facilitada**: Mudanças na lógica de banco de dados (como uma alteração na query SQL ou na estrutura da tabela) podem ser feitas no helper `add()`, sem afetar a lógica de validação ou regras de negócio do `User.add()`.

Essa estrutura modularizada, com funções distribuídas por diferentes camadas (validação de dados, lógica de aplicação e banco de dados), melhora a clareza, torna o código mais seguro e facilita testes e futuras alterações.

---

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

### O que é um decorador (funções com "@qualquer-coisa-em-cima")

Um decorador modifica ou estende o comportamento de funções ou métodos, aplicado com @decorador. Por exemplo, @staticmethod torna um método estático, permitindo chamá-lo pela classe sem instância. Isto é

```py
class Weather:
    def __init__(self):
        pass
    
    @staticmethod
    def is_rainy():
        return "it's rainy!"

print(Weather.is_rainy())
# Output: it's rainy!
```

Sem o decorador transformado aquela função em estática hávemos de instanciar um novo objeto, ainda que não o usemos para nada além do uso iminente, enquanto que com o `@staticmethod` apenas referenciamos a classe e o método.

```py
class Weather:
    def __init__(self):
        pass

    def is_rainy():
        return "it's rainy!"

weather_object = Weather()

print(weather_object.is_rainy())
# Output: it's rainy!
```

#### Classe, objeto, método estático?

- Classe: Um molde para criar objetos, definindo atributos e comportamentos (métodos).
- Instanciar: Criar um objeto baseado em uma classe.
- Métodos estáticos: Funções dentro de uma classe que não dependem de instância; chamados diretamente pela classe.

### Sistema de Recomendações

O sistema de recomendações é baseado nos empréstimos feitos por um usuário no último ano. O processo é o seguinte:

1. **Iteração sobre os empréstimos**: Vamos analisar todos os empréstimos feitos pelo usuário no último ano e coletar os gêneros dos livros que ele pegou emprestado.

2. **Ranking de gêneros mais solicitados**: A partir dessa coleta, vamos ranquear os gêneros mais solicitados pelo usuário, identificando os dois gêneros mais pedidos.

3. **Escolha do livro de contrapeso**: Para evitar recomendações tendenciosas, o sistema também selecionará o gênero menos solicitado de todos, para que ele sirva como contrapeso na recomendação.

4. **Geração de recomendações**: Com base nos dois gêneros mais solicitados e no gênero menos solicitado, o sistema irá gerar recomendações que equilibram os gostos do usuário com uma variedade de opções.

Esse sistema dará recomendações mais personalizadas, levando em consideração os padrões de leitura do usuário, sugerindo, porém, também algo novo para ampliar os seus horizontes.

## Extensões que recomendo

- [autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)
- [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens)
- [IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)
- [IntelliCode API Usage Examples](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.intellicode-api-usage-examples)
- [Import Cost](https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost)
- [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Python Indent](https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent)
- [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)
- [SQLTools SQLite](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-sqlite)

## Como começar a trabalhar com o projeto?

Para iniciar a trabalhar no projeto vocês precisam ter o git e o python instalados e configurados no computador. Como vocês estão usando Windows o método de isntalação será diferente. Definir o Git como variável de ambiente permitirá usá-lo no Command Prompt (cmd).

Para definir o Git como uma variável de ambiente no Windows, você precisa adicionar o caminho do executável git.exe ao *Path* do sistema, para assim o Windows reconheça os comandos Git:

1. Abra as configurações de variáveis de ambiente: Pesquise por “Variáveis de Ambiente” no menu Iniciar e clique em “Editar variáveis de ambiente do sistema”.

2. Adicione o caminho do Git: Na seção “Variáveis do Sistema”, selecione Path, clique em Editar, e adicione o caminho onde o Git está instalado (por exemplo, `C:\Program Files\Git\bin`ou `C:\Programas\Git\bin`).

3. Salve as alterações e reinicie o terminal para aplicar.

Voilà, isso não te acontecerá mais:
![git not recognized](https://www.partitionwizard.com/images/uploads/2021/05/git-is-not-recognized-thumbnail.png)
