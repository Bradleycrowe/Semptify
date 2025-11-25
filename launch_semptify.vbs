Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Semptify\Semptify"

' Create a nice popup
MsgBox "Starting Semptify Production Server..." & vbCrLf & vbCrLf & "Please wait...", 64, "Semptify"

' Run the PowerShell restart script hidden
WshShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Semptify\Semptify\restart_semptify.ps1""", 0, False

' Wait a moment
WScript.Sleep 3000

' Open browser
WshShell.Run "http://localhost:5000/hub", 1

' Success message
MsgBox "Semptify is starting!" & vbCrLf & vbCrLf & "Your browser will open automatically." & vbCrLf & vbCrLf & "Access at: http://localhost:5000", 64, "Semptify Started"
