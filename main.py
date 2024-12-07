from helpers.terminal import clear
from helpers import database as db
from models.books import Book
from models.lendings import Lending
from models.users import User

from time import sleep
from datetime import date


def in_range(index: int, browse_range: dict[str, int]) -> bool:
    return not (browse_range["start"] <= index < browse_range["end"])


def menu():
    while True:
        browse_range: dict[str, int] = {"start": 0, "end": 10}
        print(f"""{date.today().strftime("%A %d, %B %Y")}""")
        print("[1] Users\n[2] Books\n[3] Lendings\n[0] Exit")
        user_choice = int(input(">>> "))

        clear()


def main():
    db.drop_table(User)
    db.create_table(User)

    db.drop_table(Book)
    db.create_table(Book)

    users = [
        User(name="Ana Silva", email="ana_sorriso2022@gmail.com",
             age=25, gender="F", register_date=date(2022, 1, 4)),
        User(name="João Pereira", email="joao.adventure@gmail.com",
             age=30, gender="M", register_date=date(2022,3, 22)),
        User(name="Maria Oliveira", email="maria.olivinha@yahoo.com",
             age=27, gender="F", register_date=date(2022,6, 10)),
        User(name="Carlos Almeida", email="carlos.rockstar@outlook.com",
             age=32, gender="M", register_date=date(2022,8,5)),
        User(name="Sofia Costa", email="sofiacuriosa2022@gmail.com",
             age=29, gender="F", register_date=date(2022, 10, 18)),
        User(name="Pedro Rocha", email="pedro.monteiro@gmail.com",
             age=35, gender="M", register_date=date(2023, 1, 2)),
        User(name="Beatriz Lima", email="bia.limaflor@gmail.com",
             age=24, gender="F", register_date=date(2023,3, 14)),
        User(name="Rafael Gonçalves", email="rafael.motoqueiro@outlook.com",
             age=28, gender="M", register_date=date(2023,4, 22)),
        User(name="Lara Fernandes", email="lara.artista@gmail.com",
             age=26, gender="F", register_date=date(2023,6, 1)),
        User(name="Gabriel Moreira", email="gabriel.sonhador@yahoo.com",
             age=34, gender="M", register_date=date(2023,7, 11)),
        User(name="Luana Martins", email="lu.martins2023@gmail.com",
             age=22, gender="F", register_date=date(2023,8,8)),
        User(name="Rodrigo Souza", email="rodrigo.cervejeiro@gmail.com",
             age=31, gender="M", register_date=date(2023, 10, 15)),
        User(name="Camila Carvalho", email="camila.c@outlook.com",
             age=27, gender="F", register_date=date(2023, 11, 21)),
        User(name="Felipe Batista", email="felipe.naestrada@gmail.com",
             age=33, gender="M", register_date=date(2023, 12,5)),
        User(name="Mariana Ribeiro", email="mariana.livros@gmail.com",
             age=25, gender="F", register_date=date(2023, 12, 24)),
        User(name="Tiago Mendes", email="tiago.supermendes2024@gmail.com",
             age=30, gender="M", register_date=date(2024, 1, 2)),
        User(name="Julia Cardoso", email="juliacardoso@gmail.com",
             age=28, gender="F", register_date=date(2024,2, 13)),
        User(name="Henrique Santos", email="henrique_santos@outlook.com",
             age=35, gender="M", register_date=date(2024,3,8)),
        User(name="Isabel Castro", email="isa.castrolinda@gmail.com",
             age=26, gender="F", register_date=date(2024,4, 20)),
        User(name="Lucas Teixeira", email="lucas.tech@teixeira.net",
             age=29, gender="M", register_date=date(2024,5, 17)),
        User(name="Fernanda Monteiro", email="fer.monteiro2024@gmail.com",
             age=24, gender="F", register_date=date(2024,6,5)),
        User(name="Miguel Ribeiro", email="miguel.ribeiromoto@yahoo.com",
             age=32, gender="M", register_date=date(2024,7, 12)),
        User(name="Clara Barros", email="clarabarrosbrilho@gmail.com",
             age=23, gender="F", register_date=date(2024,8, 21)),
        User(name="Gustavo Araújo", email="gustavo.maratonista@gmail.com",
             age=27, gender="M", register_date=date(2024,9, 11)),
        User(name="Renata Dias", email="renata.sorriso@gmail.com",
             age=25, gender="F", register_date=date(2024, 10, 1)),
        User(name="Leonardo Freitas", email="leo.fritas2024@outlook.com",
             age=28, gender="M", register_date=date(2024, 10, 18)),
        User(name="Carolina Lopes", email="carol.chef@gmail.com",
             age=29, gender="F", register_date=date(2024, 10, 22)),
        User(name="Vinícius Machado", email="vinicius_gigante@gmail.com",
             age=31, gender="M", register_date=date(2024, 11, 10)),
        User(name="Letícia Vieira", email="leticia.artes@live.com",
             age=22, gender="F", register_date=date(2024, 11, 25)),
        User(name="Ricardo Monteiro", email="ricardo.nerd@gmail.com",
             age=30, gender="M", register_date=date(2024, 12, 1)),
        User(name="Amanda Gomes", email="amanda_fada@gmail.com",
             age=26, gender="F", register_date=date(2024, 12,2)),
        User(name="Eduardo Braga", email="edu_braga2024@gmail.com",
             age=34, gender="M", register_date=date(2024, 12,3)),
        User(name="Paula Nascimento", email="paula_naestrada@gmail.com",
             age=28, gender="F", register_date=date(2024, 12,4)),
        User(name="Marcos Tavares", email="marcos.t@outlook.com",
             age=33, gender="M", register_date=date(2024, 12,5)),
        User(name="Tânia Farias", email="tania.brilhante@gmail.com",
             age=25, gender="F", register_date=date(2024, 12,5)),
        User(name="Renato Pires", email="renatopires_rp@gmail.com",
             age=29, gender="M", register_date=date(2024, 12,5)),
        User(name="Patrícia Correia", email="patricia_amor@gmail.com",
             age=26, gender="F", register_date=date(2024, 12,6)),
        User(name="Diego Nunes", email="diegonunes_top@gmail.com",
             age=28, gender="M", register_date=date(2024, 12,6)),
        User(name="Carla Queiroz", email="carla.magnifica@gmail.com",
             age=27, gender="F", register_date=date(2024, 12,6)),
        User(name="André Matos", email="andrematos_ama2024@gmail.com",
             age=34, gender="M", register_date=date(2024, 12,6)),
        User(name="Manuela Paiva", email="manuela.paixao@gmail.com",
             age=23, gender="F", register_date=date(2024, 12,6)),
        User(name="Samuel Cunha", email="samuel.prodigio@gmail.com",
             age=30, gender="M", register_date=date(2024, 12,6)),
        User(name="Lúcia Santos", email="lucia_luz@gmail.com",
             age=29, gender="F", register_date=date(2024, 12,6)),
        User(name="Vítor Lopes", email="vitor.aventura@gmail.com",
             age=28, gender="M", register_date=date(2024, 12,6)),
        User(name="Joana Duarte", email="joana_d@joana.net",
             age=31, gender="F", register_date=date(2024, 12,6)),
        User(name="Daniel Souza", email="daniel_superdan@gmail.com",
             age=27, gender="M", register_date=date(2024, 12,6)),
    ]

    for user in users:
        db.add(user)

    books = [
        Book(
            title="Dom Casmurro",
            sub_title=None,
            authors="Machado de Assis",
            published_date=date(1899, 1, 1),
            synopsis="A reflection on love, jealousy, and betrayal set in Rio de Janeiro.",
            publisher="Livraria Garnier",
            isbn="9788572329304",
            genres="Fiction, Brazilian Literature",
            pages=256
        ),
        Book(
            title="Pride and Prejudice",
            sub_title=None,
            authors="Jane Austen",
            published_date=date(1813, 1, 28),
            synopsis="A timeless story of love and social expectations in 19th-century England.",
            publisher="T. Egerton, Whitehall",
            isbn="978141040349",
            genres="Fiction, Romance",
            pages=279
        ),
        Book(
            title="Memórias Póstumas de Brás Cubas",
            sub_title=None,
            authors="Machado de Assis",
            published_date=date(1881, 1, 1),
            synopsis="A satirical tale told from beyond the grave.",
            publisher="Revista Brasileira",
            isbn="9788573264673",
            genres="Fiction, Brazilian Literature",
            pages=192
        ),
        Book(
            title="Metamorphoses",
            sub_title=None,
            authors="Ovid",
            published_date=date(8, 1, 1),
            synopsis="A narrative poem chronicling Roman mythology through transformative tales.",
            publisher="Ancient Rome",
            isbn=None,
            genres="Epic, Roman Literature, Mythology",
            pages=548
        ),
        Book(
            title="O Alquimista",
            sub_title=None,
            authors="Paulo Coelho",
            published_date=date(1988, 1, 1),
            synopsis="A philosophical journey of self-discovery across the deserts of Egypt.",
            publisher="Rocco",
            isbn="9780061122415",
            genres="Fiction, Brazilian Literature, Philosophy",
            pages=208
        ),
        Book(
            title="Meditations",
            sub_title=None,
            authors="Marcus Aurelius",
            published_date=date(180, 1, 1),
            synopsis="Personal writings reflecting on Stoic philosophy.",
            publisher="Ancient Rome",
            isbn=None,
            genres="Philosophy, Roman Literature",
            pages=320
        ),
        Book(
            title="Grande Sertão: Veredas",
            sub_title=None,
            authors="João Guimarães Rosa",
            published_date=date(1956, 1, 1),
            synopsis="A complex tale of love, war, and existence in the Brazilian hinterlands.",
            publisher="José Olympio Editora",
            isbn="9788574426032",
            genres="Fiction, Brazilian Literature",
            pages=624
        ),
        Book(
            title="Inferno",
            sub_title="Divine Comedy",
            authors="Dante Alighieri",
            published_date=date(1320, 1, 1),
            synopsis="The first part of *The Divine Comedy*, depicting Dante's journey through Hell.",
            publisher="Medieval Italy",
            isbn=None,
            genres="Epic, Italian Literature, Philosophy",
            pages=432
        ),
        Book(
            title="O Primo Basilio",
            sub_title=None,
            authors="José de Alencar",
            published_date=date(1862, 1, 1),
            synopsis="A story of adultery and betrayal set in 19th-century Brazil.",
            publisher="Brazilian Literature",
            isbn=None,
            genres="Romance, Drama, Brazilian Literature",
            pages=432
        ),
        Book(
            title="A Moreninha",
            sub_title=None,
            authors="Joaquim Manuel de Macedo",
            published_date=date(1844, 5, 1),
            synopsis="A romantic novel about the complications of love and social expectations.",
            publisher="Brazilian Literature",
            isbn=None,
            genres="Romance, Brazilian Literature",
            pages=308
        ),
        Book(
            title="The Odyssey",
            sub_title=None,
            authors="Homer",
            published_date=date(800, 1, 1),
            synopsis="An epic journey of Odysseus' return home after the Trojan War.",
            publisher="Ancient Greece",
            isbn=None,
            genres="Epic, Greek Literature",
            pages=500
        ),
        Book(
            title="The Iliad",
            sub_title=None,
            authors="Homer",
            published_date=date(750, 1, 1),
            synopsis="A tale of the Greek siege of Troy and the wrath of Achilles.",
            publisher="Ancient Greece",
            isbn=None,
            genres="Epic, Greek Literature",
            pages=600
        ),
        Book(
            title="Meditations",
            sub_title=None,
            authors="Marcus Aurelius",
            published_date=date(180, 1, 1),
            synopsis="A series of personal writings by the Roman emperor on Stoicism.",
            publisher="Roman Empire",
            isbn=None,
            genres="Philosophy, Stoicism, Roman Literature",
            pages=200
        ),
        Book(
            title="The Republic",
            sub_title=None,
            authors="Plato",
            published_date=date(380, 1, 1),
            synopsis="A Socratic dialogue concerning justice, the ideal state, and the philosopher-king.",
            publisher="Ancient Greece",
            isbn=None,
            genres="Philosophy, Greek Literature",
            pages=400
        ),
        Book(
            title="Don Quixote",
            sub_title=None,
            authors="Miguel de Cervantes",
            published_date=date(1605, 1, 1),
            synopsis="The adventures of an idealistic knight and his loyal squire in medieval Spain.",
            publisher="Spanish Literature",
            isbn=None,
            genres="Romance, Spanish Literature, Satire",
            pages=1050
        ),
        Book(
            title="The Divine Comedy",
            sub_title="Inferno",
            authors="Dante Alighieri",
            published_date=date(1320, 1, 1),
            synopsis="The first part of *The Divine Comedy*, depicting Dante's journey through Hell.",
            publisher="Medieval Italy",
            isbn=None,
            genres="Epic, Italian Literature, Philosophy",
            pages=432
        ),
        Book(
            title="The Divine Comedy",
            sub_title="Purgatorio",
            authors="Dante Alighieri",
            published_date=date(1320, 1, 1),
            synopsis="The second part of *The Divine Comedy*, depicting Dante's journey through Purgatory.",
            publisher="Medieval Italy",
            isbn=None,
            genres="Epic, Italian Literature, Philosophy",
            pages=430
        ),
        Book(
            title="The Divine Comedy",
            sub_title="Paradiso",
            authors="Dante Alighieri",
            published_date=date(1320, 1, 1),
            synopsis="The final part of *The Divine Comedy*, depicting Dante's journey through Heaven.",
            publisher="Medieval Italy",
            isbn=None,
            genres="Epic, Italian Literature, Philosophy",
            pages=480
        ),
        Book(
            title="The Trial",
            sub_title=None,
            authors="Franz Kafka",
            published_date=date(1914, 1, 1),
            synopsis="A man is suddenly arrested and tried for an unnamed crime in a nightmarish bureaucratic world.",
            publisher="German Literature",
            isbn=None,
            genres="Novel, Absurdist Fiction, Philosophy",
            pages=350
        ),
        Book(
            title="The Metamorphosis",
            sub_title=None,
            authors="Franz Kafka",
            published_date=date(1915, 1, 1),
            synopsis="A man wakes up to find himself transformed into a giant insect, leading to his family's alienation.",
            publisher="German Literature",
            isbn=None,
            genres="Fiction, German Literature, Absurdist Fiction",
            pages=120
        ),
        Book(
            title="One Hundred Years of Solitude",
            sub_title=None,
            authors="Gabriel García Márquez",
            published_date=date(1967, 6, 5),
            synopsis="The story of the Buendía family, set in the fictional town of Macondo in Colombia.",
            publisher="Latin American Literature",
            isbn=None,
            genres="Magical Realism, Latin American Literature",
            pages=417
        ),
        Book(
            title="The Brothers Karamazov",
            sub_title=None,
            authors="Fyodor Dostoevsky",
            published_date=date(1880, 11, 1),
            synopsis="A philosophical novel about faith, doubt, and morality within a dysfunctional Russian family.",
            publisher="Russian Literature",
            isbn=None,
            genres="Philosophy, Russian Literature, Fiction",
            pages=796
        ),
        Book(
            title="Crime and Punishment",
            sub_title=None,
            authors="Fyodor Dostoevsky",
            published_date=date(1866, 1, 1),
            synopsis="A young man commits murder, grappling with guilt and the consequences of his actions.",
            publisher="Russian Literature",
            isbn=None,
            genres="Psychological Fiction, Russian Literature, Philosophy",
            pages=430
        ),
        Book(
            title="War and Peace",
            sub_title=None,
            authors="Leo Tolstoy",
            published_date=date(1869, 1, 1),
            synopsis="A historical novel exploring the Napoleonic Wars and the lives of Russian aristocrats.",
            publisher="Russian Literature",
            isbn=None,
            genres="Historical Fiction, Russian Literature, Epic",
            pages=1225
        ),
        Book(
            title="Anna Karenina",
            sub_title=None,
            authors="Leo Tolstoy",
            published_date=date(1877, 1, 1),
            synopsis="A tragedy about love, infidelity, and the consequences of societal pressures.",
            publisher="Russian Literature",
            isbn=None,
            genres="Fiction, Russian Literature, Drama",
            pages=864
        ),
        Book(
            title="The Communist Manifesto",
            sub_title=None,
            authors="Karl Marx, Friedrich Engels",
            published_date=date(1848, 2, 21),
            synopsis="A political pamphlet advocating for the overthrow of capitalist systems and the rise of socialism.",
            publisher="Political Philosophy",
            isbn=None,
            genres="Political Philosophy, Marxism",
            pages=90
        ),
        Book(
            title="The Wealth of Nations",
            sub_title=None,
            authors="Adam Smith",
            published_date=date(1776, 3, 9),
            synopsis="The foundational text of classical economics, analyzing wealth and the workings of markets.",
            publisher="Scottish Philosophy",
            isbn=None,
            genres="Economics, Philosophy",
            pages=1100
        ),
        Book(
            title="The Prince",
            sub_title=None,
            authors="Niccolò Machiavelli",
            published_date=date(1532, 1, 1),
            synopsis="A treatise on political philosophy, offering advice on power, statecraft, and leadership.",
            publisher="Italian Renaissance",
            isbn=None,
            genres="Political Philosophy, Italian Literature",
            pages=150
        ),
        Book(
            title="The Art of War",
            sub_title=None,
            authors="Sun Tzu",
            published_date=date(500, 1, 1),
            synopsis="An ancient Chinese text on military strategy and tactics.",
            publisher="Ancient China",
            isbn=None,
            genres="Military Strategy, Philosophy",
            pages=180
        ),
        Book(
            title="The Republic",
            sub_title=None,
            authors="Plato",
            published_date=date(380, 1, 1),
            synopsis="A Socratic dialogue concerning justice, the ideal state, and the philosopher-king.",
            publisher="Ancient Greece",
            isbn=None,
            genres="Philosophy, Greek Literature",
            pages=400
        ),
        Book(
            title="The Divine Comedy",
            sub_title="Inferno",
            authors="Dante Alighieri",
            published_date=date(1320, 1, 1),
            synopsis="Dante's journey through Hell, guided by the Roman poet Virgil.",
            publisher="Medieval Italy",
            isbn=None,
            genres="Epic, Italian Literature, Philosophy",
            pages=432
        ),
        Book(
            title="Utopia",
            sub_title=None,
            authors="Thomas More",
            published_date=date(1516, 1, 1),
            synopsis="A political and philosophical work describing a fictional island society and its customs.",
            publisher="English Renaissance",
            isbn=None,
            genres="Political Philosophy, Renaissance Literature",
            pages=200
        ),
    ]

    for book in books:
        db.add(book)

    print(db.add(User(name="Hipatia", email="hipatia@hipatia.com",
           age=25, gender="F", register_date=date(2021, 4, 15))))
    
    print(db.edit(User, id=1, age=15))

    print(f"Books: {len(db.browse(Book))}")
    for u in db.browse(Book):
        print(u)


if __name__ == "__main__":
    main()
