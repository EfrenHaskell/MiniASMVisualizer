SET fso = Wscript.CreateObject("Scripting.FileSystemObject")
SET WshShell = WScript.CreateObject("WScript.Shell")
CurrentDir = fso.GetAbsolutePathName(".")
strDsk = WshShell.SpecialFolders("Desktop")
strshortcut = strDsk & "\ASMVis.lnk"
If Not fso.FileExists(strshortcut) Then
    SET oUrlLink = WshShell.CreateShortcut(strshortcut)
    oUrlLink.TargetPath = CurrentDir & "\runProgram.vbs"
    oUrlLink.Save
End If