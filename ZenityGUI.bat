@echo off
:top
set PART=
if exist zenity.exe (
  echo "Zenity was found!"
) else (
  echo "Zenity Not Found!!!"
  timeout /t 10
  exit
)
zenity --info --title="Plug in your Samsung device" --text=" To enter download mode, Power off your device and then press and hold volume-down and power button. Then when the Download mode screen appears , press volume up to confirm entering Download mode. ( This may be differant on newer models - try typing it in to Google)"
FOR /F %%g IN ('zenity --list --no-cancel --title="Samsung Download Flasher" --text "What Partition do you want to flash?" "Boot" "Recovery" "Data" "System"') do (SET PART=%%g )
if "%PART%"=="" do (echo Quiting... && exit 0 )
:select_file
FOR /F %%g IN ('zenity --file-selection --title="Please select the *.IMG file to be flashed" --file-filter=*img') do (SET FILE=%%g && echo %FILE%)
zenity --question --icon-name=warning --text="Are you sure you want to continue? This may BRICK your device ! File %FILE% selected " --title=WARNING 
if "%ERRORLEVEL%"=="1" (
echo Quiting... && exit 0
)
mkdir temp
if "%PART%"=="Data" (
echo "Please see terminal output for progress"
heimdall/heimdall.exe flash --RECOVERY %FILE%
)
if "%PART%"=="Recovery" (
echo "Please see terminal output for progress"
heimdall/heimdall.exe flash --RECOVERY %FILE%
)
if "%PART%"=="Boot" (
echo "Please see terminal output for progress"
heimdall/heimdall.exe flash --RECOVERY %FILE%
)
if "%PART%"=="System" do (
echo "Please see terminal output for progress"
heimdall/heimdall.exe flash --RECOVERY %FILE%
)