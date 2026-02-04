#!/usr/bin/env python3

                ####################
#################      Import      #################
                ####################

import os
import sys
import subprocess
from pathlib import Path
import re
import tempfile
import shutil
import luminapy

                ####################
#################   Informations   #################
                ####################

Version     = "1.5"
Credits     = "spaghetata"
License     = "GPL3.0"


                ####################
################# Global variables #################
                ####################

var = True
welcome = "Welcome to Cenlog.\nType 'help' for seeing the functions."


                ####################
#################     Check OS     #################
                ####################

if sys.platform.startswith("win"):
    lib = f"{Path(os.getenv("APPDATA"))}/cenlog/lib.txt"

elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
    lib = Path("~/.config/cenlog/lib.txt").expanduser()

else:
    luminapy.fail(f"{os.name} is not supported.")


                ####################
#################    Functions     #################
                ####################

def main():
    command = input()

    if command == "help":
        help_menu()

    elif command == "show":
        show()

    elif command == "add":
        add()

    elif command == "delete":
        delete()

#    elif command == "change":
#        change()

    elif command == "open":
        open_log()

#    elif command == "export":
#        export()

    elif command == "exit":
        exit_script()

    else:
        luminapy.warn(f"Command '{command}' is not existing")

def help_menu():
    print(
    "=====================================HELP=====================================\n"
    "COMMAND                DEFINITION\n"
    "\n"
    "help                   list all possible commands\n"
    "show                   shows all log entrys\n"
    "add                    adds a log-file to the library\n"
    "delete                 deletes a log-file from the library\n"
    "change                 changes the name and/or the path of the log-file\n"
    "open                   opens a log-file\n"
    "export                 exports a log-file to a choosen place\n"
    "exit                   exits the programm\n"
    "=============================================================================="
    )

def show():
    with open(lib, "r") as file:
        print(file.read())

def add():
    name = input("Please enter the name of the log-file:")
    path = input("Please enter the path of the log-file:")

    if os.path.exists(path) and (path.endswith(".log") or path.endswith(".txt")):
        with open(lib, "a+") as file:
            file.write(f"{name} | {path}\n")

    else:
        luminapy.warn(f"{path} is not existing or the file is not an .txt or .log file")

def delete():
    linenumber = int(input("Please enter the linenumber you want to delete:"))

    with open(lib, "r") as file:
        lines = file.readlines()

    if linenumber <= 0 or linenumber > len(lines):
        luminapy.warn("There is something wrong with the linenumber you entered")

    else:
        pointer = 1

        for line in lines:
            if pointer == linenumber:
                del lines[pointer - 1]
                break
            pointer += 1

        with open(lib, "w") as file:
            file.writelines(lines)
            luminapy.info("Line deleted")

#def change():

def open_log():
    linenumber = int(input("Enter the linenumber of the log you want to open"))

    with open(lib, "r") as file:
        lines = file.readlines()

    pointer = 1

    if linenumber <= 0 or linenumber > len(lines):
        luminapy.warn("There is something wrong with the linenumber you entered")

    else:
        for line in lines:
            if pointer == linenumber:
                line = line.strip().split("| ")
                with open(line[1], "r") as logfile:
                    print(
                        f"\nBeginn of {line[0]}\n\n"
                        f"{logfile.read()}\n\n"
                        f"End of {line[0]}\n"
                        )


                break
            pointer += 1

#def export():

def exit_script():
    sys.exit(0)

                ####################
#################  Create lib.txt  #################
                ####################

if os.path.exists(lib):
    print(welcome)
    main()

else:
    # creates parent dirs if not existing
    os.makedirs(os.path.dirname(lib), exist_ok=True)
    with open(lib, "x") as file:
        pass

    luminapy.info(f"Directorys and files successfully created.\n{welcome}")


                ####################
#################       Loop       #################
                ####################

while var:
    main()