# Sistema Bibliotecário em Python

Autores: Douglas Lobo, Flávio Marques, Kíria Amanájas, Tiago Novo

---

- [Sistema Bibliotecário em Python](#sistema-bibliotecário-em-python)
  - [Objetivos](#objetivos)
  - [Nosso método](#nosso-método)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Explicações](#explicações)
    - [O que é um modelo](#o-que-é-um-modelo)
      - [Diferença entre `User.add()`, `db.add()` e `add()`](#diferença-entre-useradd-dbadd-e-add)
      - [Por que isso é melhor?](#por-que-isso-é-melhor)
    - [O que é um helper](#o-que-é-um-helper)
    - [O que é BREAD](#o-que-é-bread)
    - [O que é um decorador (funções com "@qualquer-coisa-em-cima")](#o-que-é-um-decorador-funções-com-qualquer-coisa-em-cima)
      - [Classe, objeto, método estático?](#classe-objeto-método-estático)
    - [Sistema de Recomendações](#sistema-de-recomendações)
  - [Extensões que recomendo](#extensões-que-recomendo)
  - [Como começar a trabalhar com o projeto?](#como-começar-a-trabalhar-com-o-projeto)
    - [Git](#git)
    - [Python](#python)
  - [Usando o Git (no projeto)](#usando-o-git-no-projeto)

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
sistema-bibliotecario/      # Diretório raiz do projeto
    helpers/                # Módulo helpers
        database.py         # Funções auxiliares para manipulação da base de dados
        queue.py            # Funções auxiliares para manipulação de filas
        notifications.py    # Funções para envio de notificações
        recommendations.py  # Funções para gerar recomendações
    models/                 # Módulo models
        audit.py            # Modelo para auditoria de ações
        lendings.py         # Modelo para empréstimos
        users.py            # Modelo para usuários
        books.py            # Modelo para livros
    main.py                 # Ponto de entrada do programa
```

## Explicações

### O que é um modelo

Um modelo é uma abstração de uma tabela da base de dados. Por exemplo, a tabela `books` terá o modelo `Book`. Isso é feito para garantir que as funções interajam com objetos do tipo `Book` e não diretamente com dados puros, como dicionários.

Um **dicionário** não é igual a um objeto `Book`. Por exemplo, o código abaixo pode ser usado para representar um livro, mas o comportamento do objeto `Book` será mais robusto e permitirá o uso de métodos específicos para manipulação de dados.

```python
book = {title: "1984", 
        publication_date: "1949-09-31", 
        synopsis: "A dystopian future.",
        publisher: "Edipro",
        genres: "Drama|Suspense|Ficção Científica"}

print(f"Livro: {book['book']}")
# Livro: 1984
```

Entretanto, isso é diferente de:

```python
book = Book(title="1984", 
        publication_date="1949-09-31", 
        synopsis="A dystopian future.",
        publisher="Edipro",
        genres="Drama|Suspense|Ficção Científica")

print(f"Livro: {book.title}")
# Livro: 1984
```

Com isso, podemos garantir uma maior organização e flexibilidade no código *e* usar métodos próprios da classe.

```python
# Enviando um email
from helpers import notifications

book = Book.read(1) # Suponhamos que 1 é o id do livro criado no exemplo anterior
user = User.read(3) # Suponhamos que 3 é o id de um usuário qualquer 

notifications.send_email(user_email=user.email, corpo_do_email=f"Obrigado {user.name}, por devolver a tempo o livro {book.title} de {book.authors}.")
# Obrigado Tiago, por devolver a tempo o livro 1984 de George Orwell.
```

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

### Git

Para iniciar a trabalhar no projeto vocês precisam ter o git e o python instalados e configurados no computador. Como vocês estão usando Windows o método de isntalação será diferente. Definir o Git como variável de ambiente permitirá usá-lo no Command Prompt (cmd).

Para definir o Git como uma variável de ambiente no Windows, você precisa adicionar o caminho do executável git.exe ao *Path* do sistema, para assim o Windows reconheça os comandos Git:

1. Abra as configurações de variáveis de ambiente: Pesquise por “Variáveis de Ambiente” no menu Iniciar e clique em “Editar variáveis de ambiente do sistema”.

2. Adicione o caminho do Git: Na seção “Variáveis do Sistema”, selecione Path, clique em Editar, e adicione o caminho onde o Git está instalado (por exemplo, `C:\Program Files\Git\bin`ou `C:\Programas\Git\bin`).

3. Salve as alterações e reinicie o terminal para aplicar.

Voilà, isso não te acontecerá mais:
![git not recognized](https://www.partitionwizard.com/images/uploads/2021/05/git-is-not-recognized-thumbnail.png)

### Python

É necessário depois de ter o Python instalado configurá-lo na *Path* do sistema Windows. Para configurar a variável de ambiente do Python no Windows, siga estes três passos:

1. **Abrir configurações de variáveis de ambiente**:
   - Pressione `Win + R`, digite `sysdm.cpl` e pressione `Enter`. No menu "Propriedades do Sistema", clique em **Configurações Avançadas do Sistema** e depois em **Variáveis de Ambiente**.

2. **Adicionar Python ao PATH**:
   - Em "Variáveis do Sistema", selecione a variável `Path` e clique em **Editar**.
   - Clique em **Novo** e adicione o caminho para a pasta onde o Python está instalado: `where python` para pegar o endereço do Python, se não for, procure aí...v

3. **Salvar e testar**:
   - Clique em **OK** para salvar. Abra o **Prompt de Comando** e digite `python --version` para verificar se a configuração foi bem-sucedida.

## Usando o Git (no projeto)

Para realmente aprenderem o git minimamente o caminho é ler o [ebook](https://git-scm.com/book/pt-pt/v2/Come%c3%a7ando-Sobre-Controle-de-Vers%c3%a3o).

1. Sempre que forem começar a trabalhar façam `git pull origin main`, isto garantirá que trabalhem com a última versão do projeto.
2. Sempre antes de fazerem `git push -u origin main` façam `git pull origin main`, isto garantirá que trabalhem com a última versão do projeto.
3. Usem `git status` para checharem como está o git.
4. Usem o `git tree` para verem a lista dos vossos commits (é um comando personalisado, para o adicionar façam `git config alias.tree "log --graph --decorate --pretty=oneline --abbrev-commit"`).
5. Ao escrever mensagens de commit, sigam estas diretrizes:
   - **Evitem mensagens genéricas ou pouco informativas**, como:

     - `fix`
     - `conserto de função`
     - `update`
     - `roberto carlos`

   - **Prefiram mensagens claras que expliquem o que o commit realmente fez.** Exemplos:

     - `implementei uma função para enviar e-mails`
     - `refatorei a função de recomendação de livros com base nas últimas solicitações do usuário`

   Não é necessário seguir uma convenção rígida. Mensagens descritivas, como `add: novo arquivo de requerimentos`, são aceitáveis, mas sempre que possível, optem por algo mais detalhado.
