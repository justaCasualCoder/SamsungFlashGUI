import sys
import subprocess
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)
class Form(QMainWindow):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("SamsungFlashGUI")
        # Create widgets
        self.label = QLabel(self)
        self.label.setText("Please select your IMG to Flash & partiton")
        self.filenameentry = QLineEdit("twrp.img")
        self.chooseimage = QPushButton("Choose Image")
        self.flash = QPushButton("Flash")
        self.buttoncheck = QComboBox()
        self.buttoncheck.addItems(["BOOT", "RECOVERY", "DATA" , "SYSTEM"])
        self.outputbox = QTextEdit()
        self.outputlabel = QLabel(self)
        self.outputlabel.setText("<center>Output:<center>")
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
        layout.addLayout( buttonbox )
        layout.addLayout( hbox )
        layout.addWidget(self.flash)
        layout.addWidget(self.outputlabel)
        layout.addWidget(self.outputlabel)
        layout.addWidget(self.outputbox)
        self.chooseimage.clicked.connect(self.Image) 
        self.flash.clicked.connect(self.flashimage)
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
    def flashimage(self):
        try:
            filename
        except NameError:
            filename = self.filenameentry.text()
        print(f"Flashing {filename} to {self.buttoncheck.currentText()}")
        print(f"heimdall flash --{self.buttoncheck.currentText()} {filename}")
        # Portions of this project are using code from the Heimdall project, developed by Benjamin Dobell and other contributors, which is licensed under the MIT License.
        heimdallbin = os.path.abspath(os.path.join(cwd,'heimdall'))
        outvar = subprocess.run([f"if [ ! -f /bin/heimdall ]; then echo 'Using Local Heimdall' && {heimdallbin} flash --{self.buttoncheck.currentText()} {filename} ; else echo 'Using /bin/heimdall' && heimdall flash --{self.buttoncheck.currentText()} {filename} ; fi"] , stdout=subprocess.PIPE , shell=True , text=True , stderr=subprocess.PIPE)
        self.outputbox.append(outvar.stdout)
        self.outputbox.append(outvar.stderr)
        if outvar.returncode != 0:
            info = ""
            if "Failed to open file" in outvar.stderr:
                print("File dosent exist")
                info = "File dosent exist"
            if "ERROR: Failed to detect compatible download-mode device." in outvar.stderr:
                print("No Device attached")
                info = "Failed to detect compatible download-mode device."
            button = QMessageBox.critical(self , "Error" , f"Heimdall failed with Exit status {outvar.returncode}: \n{info}")
    def aboutdialog(self):
        logo = os.path.abspath(os.path.join(cwd,'python-logo-only.svg'))
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




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())