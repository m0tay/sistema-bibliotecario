from datetime import date, timedelta  # noqa
from random import randint, choice
from typing import Any

from helpers import backup as bu
from helpers import database as db
from helpers import recommendations as r  # noqa
from helpers import terminal as t
from models import Audit, Book, Lending, User  # noqa: F403

page_range = {'start': 0, 'end': 10, 'pages': 0}
pages: dict[str, int] = {'at': 1, 'total': 1}
settings = {
    'page_size': 10,
    'width': 60,
}

menus = {
    'principal': {
        '1': 'Library',
        '2': 'Backups',
        '3': 'Settings',
        'q': 'Exit'
    },
    'library': {
        '1': 'Books',
        '2': 'Users',
        '3': 'Lendings',
        '4': 'Audit',
        'q': 'Go back'
    },
    'backups': {
        '1': 'See path for backup storage',
        '2': 'List backups',
        '3': 'Create a new backup',
        '4': 'Delete a backup',
        'q': 'Go back'
    },
    'settings': {
        '1': 'Width',
        '2': 'Page size',
        'q': 'Go back'
    },
    'browse': {
        '1': 'Previous page',
        '2': 'Next page',
        '3': 'Expand',
        '4': 'Add',
        'q': 'Go back'
    },
    'model_actions': {
        '1': 'Edit',
        '2': 'Delete',
        'q': 'Go back'
    },
    'deletion': {
        'delete': "Confirm deletion",
        'q': 'Go back'
    }
}


def main():
    # Database setup
    db.create_table(User)
    db.create_table(Book)
    db.create_table(Lending)
    db.create_table(Audit)

    # Backup setup
    bu.setup()

    # Load settings and display menu
    t.setup(settings)
    t.clear_cli()

    while True:
        t.menu(menus['principal'])
        user_input = input('Enter option: ')
        t.clear_cli()

        match user_input:
            case '1':  # Library menu
                while True:
                    global pages
                    global page_range
                    global at_page

                    page_range = {'start': 0, 'end': settings['page_size']}

                    pages = {'at': 1, 'total': 1}

                    t.menu(menus['library'])
                    user_input = input('Enter option: ')
                    t.clear_cli()

                    match user_input:
                        case '1':
                            while True:
                                # paginate by pagination_size
                                books = db.browse(Book)

                                # pages['total'] = len(books) // settings['page_size'] + (1 if len(books) % 10 > 0 else 0)
                                # pyright: ignore
                                pages['total'] = (
                                    len(books) + settings['page_size'] - 1) // settings['page_size']

                                for idx, b in enumerate(books):
                                    if t.in_range(idx, page_range):
                                        print(f"{f'[{b.id}': >4}] {'Title:':.<24}{
                                              b.title}")  # pyright: ignore

                                t.menu(menus['browse'], pages=pages)
                                user_input = input('Enter option: ')
                                t.clear_cli()

                                match user_input:
                                    case '1':
                                        if pages['at'] > 1:
                                            pages['at'] -= 1
                                            page_range['start'] -= settings['page_size']
                                            page_range['end'] -= settings['page_size']
                                    case '2':
                                        if pages['at'] < pages['total']:
                                            pages['at'] += 1
                                            page_range['start'] += settings['page_size']
                                            page_range['end'] += settings['page_size']
                                    case '3':
                                        book = []
                                        while not book and user_input != 'q':
                                            user_input = input(
                                                'Select book (by id): ')
                                            t.clear_cli()

                                            book = db.read(Book, id=user_input)

                                            if not book:
                                                print(
                                                    'Maybe this book does not exist')

                                        print(book if book else "")

                                        t.menu(menus['model_actions'])
                                        user_input = input('Enter option: ')
                                        t.clear_cli()

                                        match user_input:
                                            case '1':
                                                print("Editing a book")

                                                if book:
                                                    # Prompt user for inputs with current values pre-filled
                                                    title_input = get_non_empty_input(
                                                        f"Title ({book.title}): ", default=book.title)
                                                    subtitle_input = get_non_empty_input(
                                                        f"Subtitle ({book.sub_title}): ", optional=True, default=book.sub_title)
                                                    authors_input = get_non_empty_input(
                                                        f"Authors ({book.authors}): ", default=book.authors)

                                                    while True:
                                                        try:
                                                            published_date_input = input(
                                                                f"Published Date (YYYY-MM-DD) ({book.published_date}): ")
                                                            published_date = date.fromisoformat(
                                                                published_date_input) if published_date_input else book.published_date
                                                            break
                                                        except ValueError:
                                                            print(
                                                                "Invalid date format. Using default date (2000-01-01).")
                                                            published_date = book.published_date if not published_date_input else date(
                                                                2000, 1, 1)
                                                            break

                                                    synopsis_input = get_non_empty_input(
                                                        f"Synopsis ({book.synopsis}): ", default=book.synopsis)
                                                    publisher_input = get_non_empty_input(
                                                        f"Publisher ({book.publisher}): ", default=book.publisher)
                                                    isbn_input = get_non_empty_input(
                                                        f"ISBN ({book.isbn}): ", optional=True, default=book.isbn)

                                                    genres_input = get_non_empty_input(
                                                        f"Genres ({book.genres}): ", default=book.genres)

                                                    while True:
                                                        try:
                                                            pages_input = input(
                                                                f"Pages ({book.pages}): ")
                                                            pages = int(
                                                                pages_input) if pages_input.strip() else book.pages
                                                            break
                                                        except ValueError:
                                                            print(
                                                                "Invalid page number. Please enter a valid integer or press Enter to skip.")

                                                    # Edit the book record
                                                    db.edit(
                                                        Book,
                                                        id=book.id,
                                                        title=title_input,
                                                        sub_title=subtitle_input,
                                                        authors=authors_input,
                                                        published_date=published_date,
                                                        synopsis=synopsis_input,
                                                        publisher=publisher_input,
                                                        isbn=isbn_input,
                                                        genres=genres_input,
                                                        pages=pages,
                                                    )  # pyright: ignore

                                                    t.clear_cli()
                                                    break
                                                else:
                                                    print("Book not found.")
                                            case '2':
                                                t.menu(menus['deletion'])
                                                user_input = input(
                                                    'Enter option: ')
                                                t.clear_cli()

                                                match user_input:
                                                    case 'delete':
                                                        db.delete(
                                                            Book, id=book.id)
                                                    case 'q':
                                                        t.clear_cli()
                                                        break
                                                    case _:
                                                        print(
                                                            f"{'Invalid option':^{settings['width']}}")

                                            case 'q':
                                                t.clear_cli()
                                                break
                                            case _:
                                                print(
                                                    f"{'Invalid option':^{settings['width']}}")

                                    case '4':
                                        print("Adding a new book")

                                        title_input = get_non_empty_input(
                                            "Title: ")
                                        subtitle_input = get_non_empty_input(
                                            "Subtitle (optional, press Enter to skip): ", optional=True)
                                        authors_input = get_non_empty_input(
                                            "Authors: ")

                                        while True:
                                            try:
                                                published_date_input = input(
                                                    "Published Date (YYYY-MM-DD): ")
                                                published_date = date.fromisoformat(
                                                    published_date_input)
                                                break
                                            except ValueError:
                                                print(
                                                    "Invalid date format. Using default date (2000-01-01).")
                                                published_date = date(
                                                    2000, 1, 1)
                                                break

                                        synopsis_input = get_non_empty_input(
                                            "Synopsis: ")
                                        publisher_input = get_non_empty_input(
                                            "Publisher: ")
                                        isbn_input = get_non_empty_input(
                                            "ISBN (optional, press Enter to skip): ", optional=True)

                                        genres_input = get_non_empty_input(
                                            "Genres (comma-separated): ")

                                        while True:
                                            try:
                                                pages_input = input(
                                                    "Pages (optional, press Enter to skip): ")
                                                pages = int(
                                                    pages_input) if pages_input.strip() else None
                                                break
                                            except ValueError:
                                                print(
                                                    "Invalid page number. Please enter a valid integer or press Enter to skip.")

                                        db.add(Book(
                                            title=title_input,
                                            sub_title=subtitle_input,
                                            authors=authors_input,
                                            published_date=published_date,
                                            synopsis=synopsis_input,
                                            publisher=publisher_input,
                                            isbn=isbn_input,
                                            genres=genres_input,
                                            pages=pages
                                        ), verbose=True)  # pyright: ignore

                                        t.clear_cli()
                                        break

                                    case '5':
                                        user_input: Any
                                        id_to_delete: int

                                        while not isinstance(user_input, int):
                                            try:
                                                user_input = int(
                                                    input('Select book (by id) to permanently delete: '))
                                                t.clear_cli()
                                            except ValueError:
                                                print(
                                                    'Please, type a valid id')
                                                continue

                                        id_to_delete = user_input

                                        t.menu(menus['deletion'])
                                        user_input = input('Enter option: ')
                                        t.clear_cli()

                                        match user_input:
                                            case 'delete':
                                                db.delete(
                                                    Book, id=id_to_delete)
                                                print(
                                                    'Successfully deleted book')

                                            case 'q':
                                                t.clear_cli()
                                                break
                                            case _:
                                                print(
                                                    f"{'Invalid option':^{settings['width']}}")

                                    case 'q':
                                        t.clear_cli()
                                        break
                                    case _:
                                        print(
                                            f"{'Invalid option':^{settings['width']}}")

                        case '2':
                            while True:
                                # paginate by pagination_size
                                users = db.browse(User)
                                # pyright: ignore
                                pages['total'] = (
                                    len(users) + settings['page_size'] - 1) // settings['page_size']

                                for idx, u in enumerate(users):
                                    if t.in_range(idx, page_range):
                                        print(f"[{u.id}] {'Name:':.<24}{
                                              u.name}")  # pyright: ignore

                                t.menu(menus['browse'], pages=pages)
                                user_input = input('Enter option: ')
                                t.clear_cli()

                                match user_input:
                                    case '1':
                                        if pages['at'] > 1:
                                            pages['at'] -= 1
                                            page_range['start'] -= settings['page_size']
                                            page_range['end'] -= settings['page_size']
                                    case '2':
                                        if pages['at'] < pages['total']:
                                            pages['at'] += 1
                                            page_range['start'] += settings['page_size']
                                            page_range['end'] += settings['page_size']
                                    case '3':
                                        ...
                                    case '4':
                                        ...
                                    case '5':
                                        ...
                                    case '6':
                                        ...
                                    case 'q':
                                        t.clear_cli()
                                        break
                                    case _:
                                        print(f"{'Invalid option':^{
                                              settings['width']}}\n")

                        case '3':
                            while True:
                                # paginate by pagination_size
                                lendings = db.browse(Lending)
                                for idx, l in enumerate(lendings):
                                    if t.in_range(idx, page_range):
                                        # user = db.read(User, id=l.user_id)
                                        # book = db.read(Book, id=l.book_id)
                                        print(l)

                                t.menu(menus['browse'], pages=pages)
                                user_input = input('Enter option: ')
                                t.clear_cli()

                                match user_input:
                                    case '1':
                                        ...
                                    case '2':
                                        ...
                                    case '3':
                                        ...
                                    case '4':
                                        ...
                                    case '5':
                                        ...
                                    case '6':
                                        ...
                                    case 'q':
                                        t.clear_cli()
                                        break
                                    case _:
                                        print(f"{'Invalid option':^{
                                              settings['width']}}\n")

                        case '4':
                            while True:
                                # paginate by  pagination_size
                                db.browse(Audit)

                                t.menu(menus['browse'], pages=pages)
                                user_input = input('Enter option: ')
                                t.clear_cli()

                                match user_input:
                                    case '1':
                                        ...
                                    case '2':
                                        ...
                                    case '3':
                                        ...
                                    case '4':
                                        ...
                                    case '5':
                                        ...
                                    case '6':
                                        ...
                                    case 'q':
                                        t.clear_cli()
                                        break
                                    case _:
                                        print(f"{'Invalid option':^{
                                              settings['width']}}\n")

                        case 'q':
                            t.clear_cli()
                            break
                        case _:
                            print(f"{'Invalid option':^{settings['width']}}\n")

            case '2':  # Backups menu
                while True:
                    t.menu(menus['backups'])
                    user_input = input('Enter option: ')
                    t.clear_cli()

                    match user_input:
                        case '1':
                            pass
                        case '2':
                            pass
                        case '3':
                            pass
                        case '4':
                            pass
                        case 'q':
                            t.clear_cli()
                            break
                        case _:
                            print(f"{'Invalid option':^{settings['width']}}\n")

            case '3':  # Settings menu
                while True:
                    t.menu(menus['settings'])
                    user_input = input('Enter option: ')
                    t.clear_cli()

                    match user_input:
                        case '1':
                            user_input = input(
                                f'Size (current: {settings['width']}): ')

                            settings['width'] = int(user_input)

                            t.setup(settings)
                            t.clear_cli()

                        case '2':
                            user_input = input(
                                f'Size (current: {settings['page_size']}): ')

                            settings['page_size'] = int(user_input)

                            t.setup(settings)
                            t.clear_cli()
                        case 'q':
                            t.clear_cli()
                            break
                        case _:
                            print(f"{'Invalid option':^{settings['width']}}\n")

            case 'q':  # Exit
                t.clear_cli()
                break

            case _:  # Invalid option
                print(f"{'Invalid option':^{settings['width']}}\n")


def factory_users():
    genders = [None, "M", "F"]

    for i in range(1, 41):
        db.add(User(
            name=f"User {i}",
            email=f"user{i}@example.com",
            age=randint(18, 65),
            gender=choice(genders),
            register_date=date(randint(2020, 2025),
                               randint(1, 12), randint(1, 28)),
        ), verbose=True)  # pyright: ignore


def factory_books():
    from genres import genres_list
    for i in range(1, 41):
        db.add(Book(
            title=f"Book Title {i}",
            sub_title=f"Subtitle of Book {i}" if randint(0, 1) else None,
            authors=f"Author {randint(1, 10)}",
            published_date=date(randint(1990, 2025),
                                randint(1, 12), randint(1, 28)),
            synopsis=f"This is a synopsis for book {i}.",
            publisher=f"Publisher {randint(1, 10)}",
            isbn=f"{randint(1000000000, 9999999999)
                    }" if randint(0, 1) else None,
            genres=", ".join(choice(genres_list)
                             for _ in range(randint(1, 3))),
            pages=randint(100, 1000) if randint(0, 1) else None,
        ), verbose=True)  # pyright: ignore


def factory_lendings():
    for i in range(1, 41):
        user_id = randint(1, 40)
        book_id = randint(1, 40)
        from_date = date(2025, randint(1, 12), randint(1, 28))
        to_date = from_date + timedelta(days=randint(7, 30))

        db.add(Lending(
            user_id=user_id,
            book_id=book_id,
            from_date=from_date,
            to_date=to_date,
        ), verbose=True)  # pyright: ignore


def get_non_empty_input(prompt, optional=False, default=None):
    while True:
        user_input = input(prompt)
        if optional and user_input.strip() == "":
            return None  # Return None if optional and input is empty
        if user_input.strip() == "" and default is not None:
            return default  # Use the default value if input is empty
        if user_input.strip():  # Ensure non-empty input
            return user_input
        print("This field cannot be empty. Please try again.")


if __name__ == '__main__':
    main()
    # factory_users()
    # factory_books()
    # factory_lendings()
