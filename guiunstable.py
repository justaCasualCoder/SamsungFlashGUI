import sys
import subprocess
import os
import re
import requests  # Needed for Downloading TWRP
from bs4 import BeautifulSoup  # Needed for Downloading TWRP
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QProcess

cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("SamsungFlashGUI")
        self.w = None
        self.i = None
        # Create widgets
        self.label = QLabel(self)
        self.label.setText("Please select your IMG to Flash & Partiton.")
        self.filenameentry = QLineEdit("twrp.img")
        self.chooseimage = QPushButton("Choose Image")
        self.flash = QPushButton("Flash")
        self.buttoncheck = QComboBox()
        self.buttoncheck.addItems(["BOOT", "RECOVERY", "DATA", "SYSTEM"])
        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        buttonbox = QHBoxLayout()
        # Set up Menu Buttons
        aboutbutton = QAction("About", self)
        aboutbutton.setStatusTip("About this project")
        aboutbutton.triggered.connect(self.aboutdialog)
        aboutbutton.setCheckable(False)
        TWRPFlash = QAction("TWRP Flash", self)
        TWRPFlash.setStatusTip("Download / Flash TWRP")
        TWRPFlash.triggered.connect(self.TWRP_window)
        TWRPFlash.setCheckable(False)
        quitbutton = QAction("Quit", self)
        quitbutton.setStatusTip("Exit this program")
        quitbutton.triggered.connect(lambda: quit())
        quitbutton.setCheckable(False)
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(aboutbutton)
        file_menu.addAction(quitbutton)
        file_menu.addAction(TWRPFlash)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        layout.addWidget(self.label)
        hbox.addWidget(self.filenameentry)
        hbox.addWidget(self.chooseimage)
        hbox.addWidget(self.buttoncheck)
        layout.addLayout(buttonbox)
        layout.addLayout(hbox)
        layout.addWidget(self.flash)
        self.chooseimage.clicked.connect(self.Image)
        self.flash.clicked.connect(self.flash_window)

    def Image(self):
        global filename
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image Files (*.img)")
        file_dialog.setViewMode(QFileDialog.List)
        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            if filenames:
                filename = filenames[0]
                print(f"File {filename} chosen")
                self.filenameentry.setText(filename)

    def flash_window(self, checked):
        if self.w is None:
            partition = self.buttoncheck.currentText()
            image = self.filenameentry.text()
            self.w = FlashWindow()
            self.w.start_process(partition, image)
            self.w.show()

    def TWRP_window(self, checked):
        if self.i is None:
            self.i = TWRPWindow()
            self.i.show()
        else:
            self.i.close()  # Close window.
            self.i = None  # Discard reference.

    def aboutdialog(self):
        logo = os.path.abspath(os.path.join(cwd, "python-logo-only.svg"))
        text = f"""
        <p><center>SamsungFlashGUI<center><p>
        <p><center><img src="{logo}" alt=""><center></p>
        Made By <a href="https://github.com/justaCasualCoder/SamsungFlashGUI"><i>justaCasualCoder<i></a></p>
        <p>This project would not be possible without:</p>
        <p><a href="https://github.com/Benjamin-Dobell/Heimdall">Heimdall</a> (Used to Flash Images)</p>
        <p><a href="https://doc.qt.io/qtforpython-6/quickstart.html">Pyside6</a> (Used for the GUI)</p>
        <p><a href="https://www.python.org/">Python</a> (What it is coded in)</p>

        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle("About")
        dlg.setText(text)
        dlg.exec()


class FlashWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def simple_percent_parser(output):
        """
        Matches lines using the progress_re regex,
        returning a single integer for the % progress.
        """
        progress_re = re.compile("(\d+)%")
        m = progress_re.search(output)
        if m:
            pc_complete = m.group(1)
            return int(pc_complete)

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self, partition, image):
        if self.p is None:  # No process running.
            self.message("Running Heimdall!")
            self.image = image  # Needed for function handle_stderr
            self.p = (
                QProcess()
            )  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            heimdallbin = os.path.abspath(os.path.join(cwd, "heimdall/heimdall_linux"))
            if os.name == 'nt':
                print("Running on Windows!")
                print("Running heimdall.exe")
                heimdallbin = "./heimdall/heimdall.exe"
            else:
                if os.path.exists(heimdallbin):
                    print("Using Bundled Heimdall")
                    heimdallbin = "./heimdall/heimdall_linux"
                else:
                    heimdallbin = "/bin/heimdall"
            command = [f"{heimdallbin}", "flash", f"--{partition}", image]
            self.p.start(command[0], command[1:])

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        progress = self.simple_percent_parser(stdout)
        if progress:
            self.progress.setValue(progress)
        self.message(stdout)

    def simple_percent_parser(self, output):
        """
        Matches lines using the progress_re regex,
        returning a single integer for the % progress.
        """
        progress_re = re.compile("(\d+)%")
        m = progress_re.search(output)
        if m:
            pc_complete = m.group(1)
            return int(pc_complete)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)
        if "ERROR: Failed to detect compatible download-mode device." in stderr:
            print("No Device Attached!")
            info = "Failed to detect compatible download-mode device."
            self.setWindowTitle("SamsungFlashGUI: Error!")
            button = QMessageBox.critical(self, "Error", f"{info}")
            self.close()
        if "Failed to open file" in stderr:
            print("Can't find file!")
            info = f"Failed to find file: {self.image}"
            self.setWindowTitle("SamsungFlashGUI: Error!")
            button = QMessageBox.critical(self, "Error", f"{info}")
            self.close()

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: "Not running",
            QProcess.Starting: "Starting",
            QProcess.Running: "Running",
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Done Flashing!")
        self.p = None

    def __init__(self):
        super().__init__()
        self.p = None
        layout = QVBoxLayout()
        self.setWindowTitle("SamsungFlashGUI: Flashing...")
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.label = QLabel("Running Heimdall...")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.text)
        self.setLayout(layout)


class TWRPWindow(QWidget):
    def fetch_devices(self):
        devices = {}
        request = requests.get("https://twrp.me/Devices/Samsung")
        parsed_request = BeautifulSoup(request.content, "html.parser")
        device_elements = parsed_request.select("ul#post-list > p > strong > a")
        # Iterate through the 'a' tags and extract the device name and corresponding code
        for element in device_elements:
            # Extract the device name (text within the 'a' tag)
            device_name = element.text.strip()

            # Split the href and get the last part, then remove the file extension
            code = element["href"].split("/")[-1].split(".")[0]

            # Extract all content within parentheses
            parentheses_content = [content.strip() for content in device_name.split("(")[1:]]

            # Use the second set of parentheses if it exists; otherwise, use the first set of parentheses
            if len(parentheses_content) >= 2:
                code = parentheses_content[1].split(")")[0]
            else:
                code = parentheses_content[0].split(")")[0]

            # Remove spaces and convert to lowercase
            code = code.replace(" ", "").lower()

            # Add the device name and customized code to the dictionary
            devices[device_name] = code
        self.devices = devices
        self.entry.addItems(list(self.devices.keys())) 
        return devices
    def download_flash(self):
        # Huge thanks to the orginal creator - JBBgameich
        # https://github.com/JBBgameich/halium-install
        dlpagerequest = requests.get("https://dl.twrp.me/" + self.current_code)
        dlpage = BeautifulSoup(dlpagerequest.content, "html.parser")
        try:
            dllinks = dlpage.table.find_all("a")
        except:
            print("E: Couldn't find a TWRP image for " + self.current_code)
            sys.exit(1)
        dlurl = "https://dl.twrp.me" + dllinks[1]["href"].replace(".html", "")
        imgname = dlurl.split("/")[-1]
        print("I: Downloading " + dlurl)
        referer_header = {"Referer": dlurl + ".html"}
        response = requests.get(dlurl, headers=referer_header, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        current_size = 0
        with open(imgname, "wb") as f:
            for chunk in response.iter_content():
                if chunk:
                    f.write(chunk)
                    current_size += len(chunk)
                    percent = current_size / total_size * 100
                    self.progressb.setValue(percent)
                    # print(percent, end="\r")
        self.close()

        self.w = FlashWindow()
        self.w.start_process("RECOVERY", imgname)
        self.w.show()

    def __init__(self):
        super().__init__()
        self.p = None
        self.setWindowTitle("SamsungFlashGUI: Flash TWRP")
        layoutv = QVBoxLayout()
        self.get_device_button = QPushButton("Fetch Devices")
        self.get_device_button.clicked.connect(self.fetch_devices)
        self.entry = QComboBox()
        # self.entry.addItems(list(self.devices.keys())) 
        self.entry.currentIndexChanged.connect(self.device_selected)
        info1 = QLabel("Device")
        button = QPushButton("Download / Flash")
        self.progressb = QProgressBar()
        button.clicked.connect(self.download_flash)
        layoutv.addWidget(info1)
        layoutv.addWidget(self.entry)
        layoutv.addWidget(self.get_device_button)
        layoutv.addWidget(button)
        layoutv.addWidget(self.progressb)
        self.setLayout(layoutv)

    def device_selected(self, index):
        # Retrieve the selected device from the combobox
        selected_device = self.sender().itemText(index)

        # Find the corresponding custom code for the selected device from the stored devices dictionary
        selected_device_code = self.devices.get(selected_device)

        if selected_device_code is not None:
            print(f"Selected device: {selected_device}, Code: {selected_device_code}")
        else:
            print(f"Code not found for {selected_device}")
        self.current_code = selected_device_code
        


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
