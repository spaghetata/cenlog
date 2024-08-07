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

    $add_log_name = Read-Host -Prompt "Set name"
    $add_log_path = Read-Host -Prompt "Set path"

    $name_path = New-Object System.Text.StringBuilder
    [void]$name_path.Append("$log_id | ")
    [void]$name_path.Append("$add_log_name | ")
    [void]$name_path.Append("$add_log_path")

    $name_path | Add-Content -Path $BASEPATH

}

function dellog {

    Write-Host "You are going to delete a log-file entry from the library."

    $rem_id = Read-Host "Please insert the log-id you want to delete."

    # checks if the input is 0
    if ($rem_id -eq "0"){

        Write-Host "Sorry but you can not delete the default entry."

    }

    else{
        $ask_to_del = Read-Host "Do you want to delete the entry?(y/n)"

        if($ask_to_del -eq "y"){
            # filters the line with ID (regex)
            $del_line = Get-Content -Path $BASEPATH | Select-String -Pattern "^$rem_id\b"
            # deletes the filtered line above
            $content = [System.IO.File]::ReadAllText($BASEPATH).replace("$del_line`r`n", "")
            [System.IO.File]::WriteAllText($BASEPATH, $content)

            # changes the IDs after filtered line above
            $following_ids = @(Get-Content -Path $BASEPATH | Select-Object -Skip 1 | Convert-String -Example "ID | Name | Path=ID" | Where-Object { $_ -gt $rem_id})
            $new_ids = @()

            ForEach($identifier in $following_ids){

                    $new_ids += ($identifier - 1)

            }

            $new_content = [System.IO.File]::ReadAllText($BASEPATH)

            for($i = 0; $i -lt $following_ids.Length; $i++){

                $following_id = $following_ids[$i]
                $new_id = $new_ids[$i]

                $new_content = $new_content -replace "^$following_id\b", "$new_id"

            }
            [System.IO.File]::WriteAllText($BASEPATH, $new_content)

            # clears the arrays
            $following_ids = @()
            $new_ids = @()
        }

        elseif($ask_to_del -eq "n"){}

        else{
            #TODO Errorhandling
        }

    }

}

# checks if lib.txt is existing
if (Test-Path $BASEPATH ) {

    main

}

# creates dir and lib.txt
else {

    Write-Host "Creating lib.txt"
    New-Item -Path "$env:APPDATA\cenlog" -ItemType "directory"
    New-Item -Path $BASEPATH -ItemType "File"
    "ID | Name | Path" | Add-Content -Path $BASEPATH
    "0 | default | default" | Add-Content -Path $BASEPATH

}

# runs main function till programm gets stopped
while ($var_bool) {

    main

}

#TODO what if dir is existing but lib.txt is not (now you get error that the dir is already existing)
#TODO /dellog setup
#TODO /dellog regex for id input
#TODO /dellog what if the entered id is not existing
#TODO /dellog when delete a entry all following ids have to be id-1