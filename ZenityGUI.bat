@echo off
if exist zenity.exe (
  echo "Zenity was found!"
) else (
  echo "Zenity Not Found!!!"
  timeout /t 10
  exit
)
echo "Removing Temporary Directory..."
zenity --info --title="Plug in your Samsung device" --text=" To enter download mode, Power off your device and then press and hold volume-down and power button. Then when the Download mode screen appears , press volume up to confirm entering Download mode. ( This may be differant on newer models - try typing it in to Google)"
rd /s /q "temp"
FOR /F %%g IN ('zenity --list --title="Samsung Download Flasher" --text "What Partition do you want to flash?" "Boot" "Recovery" "Data" "System"') do (SET VAR=%%g && if not %ERRORLEVEL%==0 ( echo "You chose to quit!"))
echo %VAR%
