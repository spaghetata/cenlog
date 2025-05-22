import os
import sys
from pathlib import Path

var = True

# checks what os is running and then sets up the path for lib.txt
# double \\ fixes error for invalid "\" escape sequences in path
if sys.platform == "win32":
    lib = f"{Path(os.getenv("APPDATA"))}\\cenlog\\lib.txt"
else:
    lib = f"{Path.home()}\\.config\\cenlog\\lib.txt"

def main():
    command = input()

    if command == "help":
        help()

    elif command == "exit":
        exit()

    elif command == "show":
        show()

    elif command == "add":
        add()


def help():
    print(
    "=====================================HELP=====================================\n"
    "command                definition\n"
    "help                   list all possible commands\n"
    "show                   shows all log entrys\n"
    "add                    adds a log-file to the library\n"
    "delete                 deletes a log-file from the library\n"
    "change                 changes the name and/or the path of the log-file\n"
    "open                   opens a log-file\n"
    "save                   saves a log-file to a choosen place\n"
    "exit                   stops the programm\n"
    "=============================================================================="
    )

def show():
    with open(lib, "r") as file:
        content= file.read()
        print(content)

def add():
    name = input("Please enter the name of the log-file:")
    path = input("Please enter the path of the log-file:")

    if os.path.exists(path) and path.endswith(".txt"):
        with open(lib, "r+") as file:
            last_line = file.readlines()[-1]
            last_known_identifier = ""
            for char in last_line:
                if char ==" ":
                    break
                last_known_identifier += char
            new_identifier = int(last_known_identifier) + 1
            file.write(f"{new_identifier} | {name} | {path}")
    else:
        print("Path is not existing or path is not an .txt file")

def exit():
    sys.exit(0)

if os.path.exists(lib):
    main()
else:
    # creates parent dirs if not existing
    os.makedirs(os.path.dirname(lib), exist_ok=True)
    with open(lib, "x") as file:
        file.write("ID | NAME | PATH\n0 | Default | Default\n")
        print("Directorys and files successfully created.")

while var == True:
    main()


# FIXME: name can only exist once
# TODO: setup delete-function
# TODO: setup change-function
# TODO: setup open-function
# FIXME: only open logfile in r-mode
# TODO: setup export-function