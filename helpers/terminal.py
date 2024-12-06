from os import system, name


def clear():
    return system("cls") if name == "nt" else system("clear")
