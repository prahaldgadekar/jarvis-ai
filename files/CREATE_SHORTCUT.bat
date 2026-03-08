@echo off
:: Run this ONCE to create a Desktop shortcut for JARVIS
echo Creating JARVIS desktop shortcut...

set SHORTCUT=%USERPROFILE%\Desktop\JARVIS.lnk
set TARGET=%~dp0START_JARVIS.bat
set ICON=%~dp0START_JARVIS.bat

powershell -Command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%');^
   $s.TargetPath='%TARGET%';^
   $s.WorkingDirectory='%~dp0';^
   $s.WindowStyle=7;^
   $s.Description='Launch JARVIS AI Assistant';^
   $s.Save()"

echo.
echo  Done! JARVIS shortcut created on your Desktop.
echo  Double-click it anytime to start JARVIS.
echo.
pause
