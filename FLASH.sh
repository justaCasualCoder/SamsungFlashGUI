#!/bin/bash
zenity --info --title="Plug in your Samsung device" --text=" To enter download mode, Power off your device and then press and hold volume-down and power button. Then when the Download mode screen appears , press volume up to confirm entering Download mode. ( This may be differant on newer models - try typing in "YOUR-PHONE download mode" into google)"
PART=$(zenity --list \
--title="Samsung Download Flasher" \
--text "What Partition do you want to flash?" \
--radiolist \
--column "Pick" \
--column "Partition" \
FALSE "Boot" \
FALSE "Recovery" \
FALSE "Data" \
FALSE "System")
if [ $? -ne 0 ];
then
echo "Quiting..."
sleep 1
exit 0
fi
FILE=$(zenity --file-selection --title="Please select the *.IMG file to be flashed" --file-filter=*img)
case $? in
         0)
                echo "\"$FILE\" selected.";;
         1)
                echo "No file selected - Please Select a file"
                sleep 5
                exit 0 ;;
         -1)
                echo "An unexpected error has occurred.";;
esac
zenity --question --icon-name=warning --text="Are you sure you want to continue? This may BRICK your device !" --title=WARNING
if [ $? -ne 0 ];
then
echo "Quiting..."
sleep 1
exit 0
fi
case $PART in
   Recovery)
   echo "Please see terminal output for progress"
      heimdall flash --RECOVERY $FILE
      ;;
   Boot)
   echo "Please see terminal output for progress"
      heimdall flash --BOOT $FILE
      ;;
   System)
   echo "Please see terminal output for progress"
      heimdall flash --SYSTEM $FILE
      ;;
   Data)
   echo "Please see terminal output for progress"
      heimdall flash --DATA $FILE
      ;;
   *)
     echo "ERROR! - QUITING!"
     exit 0
     ;;
esac


