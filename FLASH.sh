#!/bin/bash
echo "Removing Temporary Directory ..."
rm -r temp
zenity --info --title="Plug in your Samsung device" --text=" To enter download mode, Power off your device and then press and hold volume-down and power button. Then when the Download mode screen appears , press volume up to confirm entering Download mode. ( This may be differant on newer models - try typing it in to Google)"
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
                zenity --error --text="No File Selected!" --title=ERROR
                exec ./FLASH.sh ;;
         -1)
                echo "An unexpected error has occurred."
                rm -r temp
                exit 1 ;;
esac
zenity --question --icon-name=warning --text="Are you sure you want to continue? This may BRICK your device ! File /"$FILE" selected " --title=WARNING
if [ $? -ne 0 ];
then
echo "Quiting..."
sleep 1
exit 0
fi
mkdir temp
case $PART in
   Recovery)
   echo "Please see terminal output for progress"
      heimdall flash --RECOVERY $FILE 2>&1 | tee temp/output.txt
      ;;
   Boot)
   echo "Please see terminal output for progress"
      heimdall flash --BOOT $FILE 2>&1 | tee temp/output.txt
      ;;
   System)
   echo "Please see terminal output for progress"
      heimdall flash --SYSTEM $FILE 2>&1 | tee temp/output.txt
      ;;
   Data)
   echo "Please see terminal output for progress"
      heimdall flash --DATA $FILE 2>&1 | tee temp/output.txt
      ;;
   *)
     echo "ERROR! - QUITING!"
     exit 0
     ;;
esac
egrep -q -o "ERROR: Failed to detect compatible download-mode device" temp/output.txt
if [ $? -eq 0 ];
then
zenity --error --text="No Compatible Device plugged in download mode - Restarting..."
exec ./FLASH.sh
fi
echo "Removing Temporary Directory ..."
rm -r temp
