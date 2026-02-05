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

Version     = "1.6"
Credits     = "spaghetata"
License     = "GPL3.0"
Discription = "This is a script to have a overview of your log-files."


                ####################
################# Global variables #################
                ####################

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

    elif command == "open":
        open_log()

    elif command == "export":
        export()

    else:
        luminapy.warn(f"Command '{command}' is not existing")

def check_entrys():
    with open(lib, "r") as file:
        lines = file.readlines()

        paths = []

    for line in lines:
        line = line.strip().split("| ")

        if os.path.exists(line[1]):
            pass

        else:
            paths.append(line[1])

    luminapy.warn(f"Following paths may be not correct: {paths}")

def help_menu():
    print(
    "\n=====================================HELP=====================================\n"
    "COMMAND                DEFINITION\n"
    "\n"
    "help                   list all possible commands\n"
    "show                   shows all log entrys\n"
    "add                    adds a log-file to the library\n"
    "delete                 deletes a log-file from the library\n"
    "open                   opens a log-file\n"
    "export                 exports a log-file to a choosen place\n"
    "==============================================================================\n"
    )

def show():
    with open(lib, "r") as file:
        print(
            "\n===\n"
            f"{file.read()}\n"
            "===\n"
            )

def add():
    name = input("Please enter the name of the log-file: ")
    path = input("Please enter the path of the log-file: ")

    if os.path.exists(path) and (path.endswith(".log") or path.endswith(".txt")):
        with open(lib, "a+") as file:
            file.write(f"{name} | {path}\n")

    else:
        luminapy.warn(f"{path} is not existing or the file is not an .txt or .log file.")

def delete():
    show()
    linenumber = int(input("Please enter the linenumber you want to delete: "))

    with open(lib, "r") as file:
        lines = file.readlines()

    if linenumber <= 0 or linenumber > len(lines):
        luminapy.warn("There is something wrong with the linenumber you entered.")

    else:
        pointer = 1

        for line in lines:
            if pointer == linenumber:
                del lines[pointer - 1]
                break
            pointer += 1

        with open(lib, "w") as file:
            file.writelines(lines)
            luminapy.info("Line deleted.")

def open_log():
    show()
    linenumber = int(input("Enter the linenumber of the log you want to open: "))

    with open(lib, "r") as file:
        lines = file.readlines()

    pointer = 1

    if linenumber <= 0 or linenumber > len(lines):
        luminapy.warn("There is something wrong with the linenumber you entered.")

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

def export():
    show()
    linenumber = int(input("Please enter the linenumber of the log you want to export: "))
    dest = input("Please enter the destination: ")

    with open(lib, "r") as file:
        lines = file.readlines()

    pointer = 1

    if linenumber <= 0 or linenumber > len(lines):
        luminapy.warn("There is something wrong with the linenumber you entered.")

    else:
        for line in lines:
            if pointer == linenumber:
                line = line.strip().split("| ")

                if os.path.exists(line[1]) and os.path.exists(dest):
                    shutil.copy2(line[1], dest)
                    luminapy.info(f"Copied file to {dest}.")

                else:
                    luminapy.warn("The paths you entered arent correct. Please check!")

                break

            pointer += 1


                ####################
#################       Loop       #################
                ####################

if __name__ == "__main__":

    if os.path.exists(lib):
        pass

    else:
        # creates parent dirs if not existing
        os.makedirs(os.path.dirname(lib), exist_ok=True)
        with open(lib, "x") as file:
            pass

        luminapy.info("Directorys and files successfully created.")

    print(welcome)
    check_entrys()

    try:
        while True:
            main()

    except KeyboardInterrupt:
        luminapy.info("Script manually stopped by user.")