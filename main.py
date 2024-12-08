from helpers import terminal as t
from helpers import database as db
from models.books import Book
from models.lendings import Lending
from models.users import User

from time import sleep
from datetime import date

main_menu = {
    "1": {"text": "Library", "func": t.submenu({
        "1": {"text": "Users", "func": t.submenu({
            "1": {"text": f"Browse 10 more", "func": lambda: False},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "0": {"text": "Go Back", "func": lambda: True}
        })},

        "2": {"text": "Books", "func": t.submenu({
            "1": {"text": f"Browse 10 more", "func": lambda: False},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "0": {"text": "Go Back", "func": lambda: True}
        })},

        "3": {"text": "Lending", "func": t.submenu({
            "1": {"text": f"Browse 10 more", "func": lambda: False},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "0": {"text": "Go Back", "func": lambda: True}
        })},
        "0": {"text": "Go Back", "func": lambda: True}
    })},
    "2": {"text": "Backups", "func": t.submenu({
        "1": {"text": "Path of current backup", "func": lambda: print("backup/backup_12.sqlite3")},
        "2": {"text": "Back Up", "func": lambda: print("Preparing back up...")},
        "3": {"text": "Delete Backup", "func": lambda: print("Deleting back up...")},
        "0": {"text": "Go Back", "func": lambda: True}
    })},
    "3": {"text": "Settings", "func": lambda: False},
    "0": {"text": "Exit", "func": lambda: True},
}


def main():
    t.clear_cli()
    t.menu(main_menu)


if __name__ == "__main__":
    main()
