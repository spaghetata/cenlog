# Script for a central logging overview
# Script by N.Sedlaczek

Write-Host "
Welcome to cenlog.`r
Type /help for help."

# Basepath vor lib.txt
$BASEPATH = "$env:APPDATA\cenlog\lib.txt"
$VARBOOL = $true
$READFILE = [System.IO.File]::ReadAllText($BASEPATH)

# define Functions
function main{

    $command = Read-Host

    if ($command -eq "help"){

        help

    }

    elseif ($command -eq "show"){

        showlogs

    }

    elseif ($command -eq "add"){

        addlog

    }

    elseif ($command -eq "delete") {

        dellog

    }

    elseif ($command -eq "change") {

        chlog

    }

    elseif ($command -eq "open"){

        open

    }

    elseif ($command -eq "save") {

        save

    }

    elseif ($command -eq "exit"){

        exit_script

    }

    else{

        Write-Host "Invalid command"

    }

}

function help {

    Write-Host "
    =====================================HELP=====================================`r
    command                 definition`r
    help                   list all possible commands`r
    show                   shows all log entrys`r
    add                    adds a log-file to the library`r
    delete                 deletes a log-file from the library`r
    change                 changes the name and/or the path of the log-file`r
    open                   opens a log-file`r
    save                   saves a log-file to a choosen place`r
    exit                   stops the programm`r
    =============================================================================="

}

function showlogs {

    Write-Host "`n$READFILE"

}

function addlog {
    Write-Host "You are going to add a new log-file entry to the library."

    $get_last_id = Get-Content -Path $BASEPATH -Tail 1 | Convert-String -Example "ID | Name | Path=ID"
    $log_id = [int]$get_last_id + 1

    $add_log_name = Read-Host -Prompt "Set name"
    $add_log_path = (Read-Host -Prompt "Set path")

    $new_entry = New-Object System.Text.StringBuilder
    [void]$new_entry.Append("`r$log_id | ")
    [void]$new_entry.Append("$add_log_name | ")
    [void]$new_entry.Append("$add_log_path")

    $new_entry | Add-Content -Path $BASEPATH

}

function dellog {

    Write-Host "You are going to delete a log-file entry from the library."

    $rem_id = Read-Host "Please insert the log-id you want to delete."

    # checks if the input is 0
    if ($rem_id -eq "0"){

        Write-Host "Sorry but you can not delete the default entry."

    }

    # only allow nummeric ids for searching
    elseif ($rem_id -match "[1-9]+"){
        $ask_to_del = Read-Host "Do you want to delete the entry?(y/n)"

        if($ask_to_del -eq "y"){
            # filters the line with ID (regex)
            $del_line = Get-Content -Path $BASEPATH | Select-String -Pattern "^$rem_id\b.*$"
            # deletes the filtered line
            $new_content = $READFILE -replace "$del_line", ""

            # changes the IDs after filtered line above
            $following_ids = @(Get-Content -Path $BASEPATH | Select-Object -Skip 1 | Convert-String -Example "ID | Name | Path=ID" | Where-Object { $_ -gt $rem_id})
            $new_ids = @()

            ForEach($identifier in $following_ids){

                    $new_ids += ($identifier - 1)

            }

            for($i = 0; $i -lt $following_ids.Length; $i++){

                $new_content = $new_content -replace "\b$following_ids[$i]\b", "$new_ids[$i]"

            }
            Write-Host $new_content
            exit_script

            [System.IO.File]::WriteAllText($BASEPATH, $new_content)

            # clears the arrays
            $following_ids = @()
            $new_ids = @()
        }

        elseif($ask_to_del -eq "n"){}

    }

    else {

        Write-Host "That is not an ID. Please try again!"

    }

}

function chlog{

    $ask_for_entry = Read-Host "Which log-entry do you want to change? Please enter the name."

    $get_entry = Get-Content -Path $BASEPATH | Select-Object -Skip 1 | Select-String -Pattern "$ask_for_entry\b"
    $get_length = ($get_entry | Measure-Object -Character).Characters

    #checks if stringlength is even because you cant print "=" 12.5 times for example
    if($get_length % 2 -ne 0){

        $get_length = $get_length + 1

    }

    else{

    }

    Write-Host "
    $("=" * ($get_length/2))Entry$("=" * ($get_length/2))`r
    $get_entry`r
    $("=" * ($get_length + 5))`r"

    $ask_for_change = Read-Host "What do you want to change?(name/path)"

    if($ask_for_change -eq "name"){

        $get_new_name = Read-Host "Please enter the new name."

        $name_to_replace = ($get_entry -split "|")[1].Trim()
        $changed_name = [regex]::Replace($READFILE, "\b$name_to_replace\b", $get_new_name) #TODO does also replace the name in path
        Write-Host $changed_name
        [System.IO.File]::WriteAllText($BASEPATH, $changed_name)


    }

    elseif($ask_for_change -eq "path"){

    }

    else{

        Write-Host "Invalid input"

    }

}

function open{

    $ask_for_log = Read-Host "What log-file do you want to open? Please enter the name."

    $get_log = Get-Content -Path $BASEPATH | Select-Object -Skip 1 | Select-String -Pattern "$ask_for_log\b"
    $get_path = $get_log | Convert-String -Example "ID | Name | Path=Path"

    $openlog = [System.IO.File]::ReadAllText($get_path)
    Write-Host "$openlog"

}

function save{

    $ask_for_safe = Read-Host "What log-file do you want to save? Please enter the Name."

    $get_log_entry = Get-Content -Path $BASEPATH | Select-Object -Skip 1 | Select-String -Pattern "$ask_for_safe\b"
    $get_orig_path = $get_log_entry | Convert-String -Example "ID | Name | Path=Path"

    $ask_for_newpath = Read-Host "Where do you want to save the log file? Please enter Path."

    if(Test-Path $ask_for_newpath){

        Copy-Item -Path $get_orig_path -Destination $ask_for_newpath

    }

    else {

        Write-Host "Sorry but the path you entered is incorrect or not existing. Please check and try again."

    }

}

function exit_script{

    exit

}

# checks if lib.txt is existing
if (Test-Path $BASEPATH ) {

    main

}

# creates dir and lib.txt
else {

    Write-Host "Creating lib.txt"
    New-Item -Path "$env:APPDATA\cenlog" -ItemType "Directory"
    New-Item -Path $BASEPATH -ItemType "File"
    "ID | Name | Path" | Add-Content -Path $BASEPATH
    "0 | default | default" | Add-Content -Path $BASEPATH

}

# runs main function till programm gets stopped
while ($VARBOOL) {

    main

}

#TODO:              what if dir is existing but lib.txt is not (now you get error that the dir is already existing)
#TODO: delete       setup
#TODO: change       setup

#TODO: add          name can only exist once
#FIXME: delete      does not change id because ReadAllText dont accept regex
#FIXME: delete      does not delete last line
#FIXME:             lib.txt needs to be updated when content gets requested
#TODO: delete       what if the entered id is not existing
#TODO: delete       when delete a entry all following ids have to be id-1