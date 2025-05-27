#!/usr/bin/env python3

                 ####################
##################      Import      ##################
                 ####################

import os
import sys
import subprocess
from pathlib import Path
import re
import tempfile
import shutil

                 ####################
##################   Informations   ##################
                 ####################

Version     = "1.2"
Credits     = "spaghetata"
License     = "GPL3.0"


                 ####################
################## Global variables ##################
                 ####################

var = True


                 ####################
##################     Check OS     ##################
                 ####################

if sys.platform.startswith("win"):
    lib = f"{Path(os.getenv("APPDATA"))}\\cenlog\\lib.txt"
    def open_terminal(value):
        subprocess.Popen(["start", "cmd.exe", "/K", sys.executable, value], shell=True)

elif sys.platform.startswith("darwin"):
    lib = f"{Path.home()}\\.config\\cenlog\\lib.txt"
    def open_terminal(value):
        default_shell = os.environ.get("SHELL", "/bin/bash")
        subprocess.Popen([default_shell, "-c", sys.executable, value])

elif sys.platform.startswith("linux"):
    lib = f"{Path.home()}\\.config\\cenlog\\lib.txt"
    def open_terminal(value):
        default_shell = os.environ.get("SHELL", "/bin/bash")
        subprocess.Popen([default_shell, "-c", sys.executable, value ])

else:
    print(f"{os.name} is not supported.")


                 ####################
##################    Functions     ##################
                 ####################

def check_id(identifier):
    pattern = rf"^\b{identifier}\b"

    with open(lib, "r") as file:
        lines = file.readlines()

    for line in lines:
        if re.match(pattern, line):
            return True

    return False

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

    elif command == "change":
        change()

    elif command == "open":
        open_log()

    elif command == "export":
        export()

    elif command == "exit":
        exit_script()

    else:
        print(f"Command {command} is not existing")

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
            file.write(f"\n{new_identifier} | {name} | {path}")

    else:
        print(f"{path} is not existing or path is not an .txt file")

def delete():
    identifier = input("Please enter the id of the entry you want to delete:")

    is_existing = check_id(identifier)

    if is_existing and identifier != "0":
        with open(lib, "r") as file:
            lines = file.readlines()

        new_lines = []
        deleted_line_index = None

        for i, line in enumerate(lines):

            line_id = line.split()[0] if line else ""

            if line_id == identifier:
                deleted_line_index = i
                continue

            new_lines.append(line)

        for idx in range(deleted_line_index, len(new_lines)):
            line = new_lines[idx]

            parts = line.split(maxsplit = 1)

            if not parts:
                continue

            try:
                old_id = int(parts[0])
            except ValueError:
                continue

            new_id = old_id - 1
            rest_of_line = parts[1] if len(parts) > 1 else ""

            new_line = f"{new_id} {rest_of_line}"

            new_lines[idx] = new_line

        with open(lib, "w") as file:
            file.writelines(new_lines)

    elif identifier == "0":
        print("You cant delete the default entry!")

    else:
        print(f"There is no entry with the id {identifier}.")

def change():
    show()

    identifier = input("\nWhich entry do you want to change?\n\n")

    is_existing = check_id(identifier)

    if is_existing:

        change_name = input("Please enter new name (leave empty for no change):")
        if change_name:

            with open(lib, "r") as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                if re.match(rf"^\b{identifier}\b", line):
                    parts = [p.strip() for p in line.split("|")]
                    parts[1] = f"{change_name}"
                    updated_entry = " | ".join(parts)
                    updated_lines.append(f"{updated_entry}\n")

                else:
                    updated_lines.append(line)

            with open(lib, "w") as file:
                file.writelines(updated_lines)

            del file, lines, line, parts, updated_entry, updated_lines

        change_path = input("Please enter new path (leave empty for no change):")
        if change_path:
            if os.path.exists(change_path) and change_path.endswith(".txt"):
                with open(lib, "r") as file:
                    lines = file.readlines()

                updated_lines = []
                for line in lines:
                    if re.match(rf"^\b{identifier}\b", line):
                        parts = [p.strip() for p in line.split("|")]
                        parts[2] = f"{change_path}"
                        updated_entry = " | ".join(parts)
                        updated_lines.append(f"{updated_entry}\n")

                    else:
                        updated_lines.append(line)

                with open(lib, "w") as file:
                    file.writelines(updated_lines)

            else:
                print(f"{change_path} is not existing or path is not an .txt file")

    else:
        print(f"There is no entry with the id {identifier}.")

def open_log():
    show()

    identifier = input("\nPlease enter the id of the log-file you want to open:")

    is_existing = check_id(identifier)

    if is_existing:

        with open(lib, "r") as file:
            lines = file.readlines()

        for line in lines:
            if re.match(rf"^\b{identifier}\b", line):
                parts = [p.strip() for p in line.split("|")]

                if os.path.exists(parts[2]):
                    with open(parts[2], "r") as file:
                        content = file.read()

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
                            tmp.write(f"print({repr(content)})")

                        open_terminal(tmp.name)

                else:
                    print(f"{parts[2]} is not existing")

    else:
        print(f"There is no entry with the id {identifier}.")

def export():
    show()

    identifier = input("\nPlease enter the id of the log-file you want to export:")

    is_existing = check_id(identifier)

    if is_existing:

        with open(lib, "r") as file:
            lines = file.readlines()

        for line in lines:
            if re.match(rf"^\b{identifier}\b", line):
                parts = [p.strip() for p in line.split("|")]
                dst = input(f"Please enter path of destination: ")

                if os.path.exists(parts[2]) and os.path.exists(dst):
                    shutil.copy2(parts[2], dst)
                    print(f"Export to {dst} successfull")

                else:
                    print("One of the path is not existing")

    else:
        print(f"There is no entry with the id {identifier}.")

def exit_script():
    sys.exit(0)


                 ####################
##################  Create lib.txt  ##################
                 ####################

if os.path.exists(lib):
    print(
    "Welcome to Cenlog.\n"
    "Type 'help' for seeing the functions."
    )
    main()

else:
    # creates parent dirs if not existing
    os.makedirs(os.path.dirname(lib), exist_ok=True)
    with open(lib, "x") as file:
        file.write("ID | NAME | PATH\n0 | Default | Default")
        print("Directorys and files successfully created.")


                 ####################
##################       Loop       ##################
                 ####################

while var == True:
    main()
