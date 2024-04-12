SET fso = Wscript.CreateObject("Scripting.FileSystemObject")
SET WshShell = WScript.CreateObject("WScript.Shell")
CurrentDir = fso.GetAbsolutePathName(".")
Command = "cmd /c python " & CurrentDir & "/StepUX.py"
WshShell.Run Command, 0, True