# SamsungFlashGUI
A Python Script that can be used to easily flash .img files to any Samsung phone
### Running
Download the file corresponding to your OS. 

To run on Windows , open a Command Prompt in the directory where it was downloaded and run SamsungFlashGUI.exe

To run on Linux , open a Terminal in the directory where it was downloaded and run ./SamsungFlashGUILinux
#### Building
In order to build the Python file into a portable executable , you have to run the following command:

On Windows 
```
pyinstaller --onefile --noconsole --add-data "EXACTPATHTOPARENTDIR/heimdall:heimdall" SamsungFlashGUI.py 
```
On Linux
```
pyinstaller --onefile --noconsole --add-data "$(pwd)/heimdall:heimdall" SamsungFlashGUI.py
```
###### Screenshots
<img src="Images/FileSelect.png" width="600px" > <img src="Images/SelectPart.png" width="600px" >
## Instructions