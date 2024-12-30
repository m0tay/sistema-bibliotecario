import os
import shutil
from helpers import database as db
from helpers import backup as bu
from helpers import recommendations as r
from helpers import terminal as t
from models import *  # noqa: F403
from datetime import date


main_menu = {
    "1": {"text": "Library", "func": t.submenu({
        "1": {"text": "Users", "func": t.submenu({
            "1": {"text": "Browse more", "func": lambda: print("Read selected")},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "6": {"text": "Recommend", "func": lambda: r.health()},
            "0": {"text": "Go Back", "func": lambda: True}
        })},

        "2": {"text": "Books", "func": t.submenu({
            "1": {"text": "Browse more", "func": lambda: False},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "0": {"text": "Go Back", "func": lambda: True}
        })},

        "3": {"text": "Lending", "func": t.submenu({
            "1": {"text": "Browse more", "func": lambda: False},
            "2": {"text": "Read", "func": lambda: print("Read selected")},
            "3": {"text": "Edit", "func": lambda: print("Edit selected")},
            "4": {"text": "Add", "func": lambda: print("Add selected")},
            "5": {"text": "Delete", "func": lambda: print("Delete selected")},
            "0": {"text": "Go Back", "func": lambda: True}
        })},
        "0": {"text": "Go Back", "func": lambda: True}
    })},
    "2": {"text": "Backups", "func": t.submenu({
        "1": {"text": "Path of backups", "func": lambda: bu.path()},
        "2": {"text": "Back Up", "func": lambda: bu.backup()},
        "3": {"text": "Delete Oldest Backup", "func":t.submenu({
            "delete": {"text": "Delete", "func": lambda: bu.delete_oldest_backup()},
            "0": {"text": "Go Back", "func": lambda: lambda: False}
        }, "Do you are sure to delete the oldest backup?")},
        "4": {"text": "Load last backup", "func": lambda: bu.load_backup()},
        "5": {"text": "List all backups", "func": lambda: bu.list_backups()},
        "0": {"text": "Go Back", "func": lambda: True}
    })},
    "3": {"text": "Settings", "func": lambda: False},
    "0": {"text": "Exit", "func": lambda: True},
}


def main():

    # database
    db.create_table(User)
    db.create_table(Book)
    db.create_table(Lending)

    # backup
    bu.setup()


    # load settings


    t.clear_cli()
    t.menu(main_menu)


if __name__ == "__main__":
    main()
