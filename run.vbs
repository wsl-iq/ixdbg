' *****************************************************
' Script Name : RunPythonApp.vbs
' Description : VBScript to safely run a Python script.
' Author      : Mohammed Al-Baqer
' License     : MIT License
' Created     : 2025-06-01
' *****************************************************

Option Explicit

' Get the full path to the current script directory
Dim fso, currentDir, pythonScriptPath, shell, command

Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Construct the full path to the Python script
pythonScriptPath = currentDir & "\app\index.py"

' Create WScript Shell object
Set shell = CreateObject("WScript.Shell")

' Change working directory to "app"
shell.CurrentDirectory = currentDir & "\app"

' Build the command to run the Python script
command = "python index.py"

' Run the Python script (1 = show window, False = don't wait)
shell.Run command, 1, False

' Clean up
Set shell = Nothing
Set fso = Nothing

' Exit the script
WScript.Quit 0

' End of script
' *****************************************************
' This script is designed to run a Python application located in the "app" directory.
' It changes the working directory to "app" and executes the Python script "index.py".
' Ensure that Python is installed and available in the system PATH.
' The script does not wait for the Python script to finish executing.
' *****************************************************
