# SamsungFlashGUI

A Python Script that can be used to easily flash .img files to any Samsung phone. 

`gui.py` is the main file , and `guiunstable.py` is a updated but unstable version.

See this [Github Project Page](https://github.com/users/justaCasualCoder/projects/1/views/1) for future goals.
### Running

Install PySide6

```bash
pip install PySide6
```

Install Heimdall (Example on Debian):

```bash
sudo apt install heimdall
```

Download / save `gui.py` and run it. 

#### Building

In order to build the Python file into a portable executable , you have to install [Pyinstaller](https://pyinstaller.org/en/stable/) and run the following command:

```bash
pyinstaller --onefile --noconsole --add-binary "/bin/heimdall:." --add-data "$(pwd)/python-logo-only.svg:." gui.py
```

# Credits

The following programs were used in the code:

[Heimdall](https://github.com/Benjamin-Dobell/Heimdall) (Used to Flash Images)

[Pyside6](https://doc.qt.io/qtforpython-6/quickstart.html) (Used for the GUI)

[Python](https://www.python.org/) (What it is coded in)

# Windows
When I first made this, it only worked on Linux. I am now starting to add Windows 10/11 support as well. If you try running the program on Windows, it expects that you have extracted `heimdall` into `heimdall/`. You can follow `heimdall/README.txt` for installing drivers. Here is a snippet:

Driver Installation Instructions:

1. Put your device into download mode and plug it in.

2. Run zadig.exe included in the Drivers subdirectory.

3. From the menu chose Options -> List All Devices.

4. From the USB Device list chose "Samsung USB Composite Device".

5. Press "Install Driver", click "Yes" to the prompt and if you receive
       a message about being unable to verify the publisher of the driver.
       Click "Install this driver software anyway".

6. Done

# Screenshots

![](screenshots/main_window.png "Main Window")

![](screenshots/about_window.png "About Window")

# Why?

- I wanted a easy way to flash `*IMG`'s to Samsung devices

- The already made Heimdall-Frontend is awesome , but was overcomplicated for me.

- WHY NOT
