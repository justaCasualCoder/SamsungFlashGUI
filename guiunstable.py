import sys
import subprocess
import os
import re
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTextEdit,
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
        # AutoDetctedButton = QAction("Auto Mode", self)
        # AutoDetctedButton.setStatusTip("Auto-Detcted Device")
        # AutoDetctedButton.triggered.connect(self.detectdevice)
        # AutoDetctedButton.setCheckable(False)
        quitbutton = QAction("Quit", self)
        quitbutton.setStatusTip("Exit this program")
        quitbutton.triggered.connect(lambda: quit())
        quitbutton.setCheckable(False)
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(aboutbutton)
        file_menu.addAction(quitbutton)
        # file_menu.addAction(AutoDetctedButton)
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

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

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
        button = dlg.exec()

    # def detectdevice(self):
    #     print("")


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
            command = ["heimdall", "flash", f"--{partition}", image]
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
            button = QMessageBox.critical(self, "Error", f"{info}")
        if "Failed to open file" in stderr:
            print("Can't find file!")
            info = f"Failed to find file: {self.image}"
            button = QMessageBox.critical(self, "Error", f"{info}")

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


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())