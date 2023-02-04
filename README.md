# SamsungFlashGUI
A Script that can be used to easily flash .img files to any samsung phone using Linux (Windows is being developed)
##### Screenshots
<img src="Images/FileSelect.png" width="600px" > <img src="Images/SelectPart.png" width="600px" >
## Instructions
#### Windows
Download the Windows.zip from the releases section and extract it. Then enter the folder that you extracted the zip to and run the zadig tool inside the heimdall directory. Then go to the top of of the program and press Options/List all devices. After that go to the device slection area and select your device. It should be something like MSM****. Then cycle through the driver,s and replace each driver. 
After You have done this, go to the parent folder ( the directory that you unzipped to) and run flashgui.bat .the program will guide you through the rest
#### Linux
On Linux, It,s pretty much plug-and-play ( only Zenity ,git , and heimdall are required)... run the following to run the script without even downloading it!
```
bash <( curl -s https://raw.githubusercontent.com/justaCasualCoder/SamsungFlashGUI/main/FLASH.sh)
```
