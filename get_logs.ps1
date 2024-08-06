# Script for a central logging overview
# Script by N.Sedlaczek

Write-Host "Welcome to cenlog."
Write-Host "Type /help for help."

# Basepath vor lib.txt
$BASEPATH = "$env:APPDATA\cenlog\lib.txt"
$var_bool = "true"

# define Functions
function main{

    $command = Read-Host

    if ($command -eq "/help"){

        help_menu

    }

    elseif ($command -eq "/addlog"){

        add_log

    }

    elseif ($command -eq "/dellog") {

        dellog

    }

    else{

    }

}

function help_menu {

    Write-Host "=====================================HELP====================================="
    Write-Host "command                 definition"
    Write-Host "/help                   list all possible commands"
    Write-Host "/addlog                 adds a log-file to the library"
    Write-Host "/dellog                 deletes a log-file from the library"
    Write-Host "/chlog                  changes the name and/or the path of the log-file"
    Write-Host "/open                   opens a log-file"
    Write-Host "/close                  closes a log-file"
    Write-Host "/clear                  clears a log file"
    Write-Host "/safe                   safes a log-file to a choosen place"
    Write-Host "/exit                   stops the programm"
    Write-Host "=============================================================================="

}

function add_log {
    Write-Host "You are going to add a new log-file entry to the library."

    $get_last_id = Get-Content -Path $BASEPATH -Tail 1 | Convert-String -Example "ID | Name | Path=ID"
    $log_id = [int]$get_last_id + 1

    $add_log_name = Read-Host -Prompt "Set name: "
    $add_log_path = Read-Host -Prompt "Set path: "

    $name_path = New-Object System.Text.StringBuilder
    [void]$name_path.Append("$log_id | ")
    [void]$name_path.Append("$add_log_name | ")
    [void]$name_path.Append("$add_log_path")

    $name_path | Add-Content -Path $BASEPATH

}

function dellog {

    Write-Host "You are going to delete a log-file entry from the library."
    $ask_for_del = Read-Host "Are you sure to delete a log-file entry? (y/n)"

    if ($ask_for_del -eq "y"){

        $rem_id = Read-Host "Please insert the log-id you want to delete."
        $get_line = Get-Content -Path $BASEPATH | Select-String -Pattern "$rem_id | * | *"
        $get_line.Replace("$rem_id | * | *","")

    }

    else{}

}

# checks if lib.txt is existing
if (Test-Path $BASEPATH ) {

    main

}

# creates dir and lib.txt
else {

    Write-Host Creating library
    New-Item -Path "$env:APPDATA\cenlog" -ItemType "directory"
    New-Item -Path $BASEPATH -ItemType "File"
    "ID | Name | Path" | Add-Content -Path $BASEPATH
    "0 | deflaut | default" | Add-Content -Path $BASEPATH

}

# runs main function till programm gets stopped
while ($var_bool) {

    main

}

#TODO setup dellog
#TODO unable to delete lib.txt entry with id 0
#TODO when delete a entry all following ids have to be id-1