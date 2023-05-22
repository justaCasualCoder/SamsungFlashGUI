import os
import argparse
import platform
import shutil
import sys
import subprocess
import qdarktheme
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLabel, QMessageBox
from qdarktheme import load_stylesheet
parser = argparse.ArgumentParser(description='Samsung Flash GUI Script (This was only possible becasue of Heimdall and Pyside6!)')
parser.add_argument('--dark', action='store_true', help='use dark mode' , default=0)
parser.add_argument('--easy', action='store_true', help='Easy mode')
args = parser.parse_args()
app = QApplication.instance() or QApplication([])
app.setStyleSheet(qdarktheme.load_stylesheet("auto"))
qdarktheme.enable_hi_dpi()
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
cwd = os.path.dirname(os.path.abspath(__file__))
operating_system = platform.system()
if operating_system == 'Linux':
    print("You are running Linux!")
elif operating_system == 'Windows':
    print("You are running Windows")
else:
    print("Unsupported operating system:", operating_system)
    exit()
if args.easy:
    from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
    from adb_shell.auth.sign_pythonrsa import PythonRSASigner
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048)
    print(key)
    from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
    from adb_shell.auth.sign_pythonrsa import PythonRSASigner
    device = AdbDeviceUsb()
    device.connect(rsa_keys=["~/.android/adbkey"])
    codename = device.shell("getprop ro.product.device")
    subprocess.call(['python', 'download-twrp.py'] , codename)
# Select the partition to be flashed
class PartitionDialog(QDialog):
    def __init__(self, partitions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Samsung Download Flasher")
        self.result = None
        self.partitions = partitions

        self.create_widgets()

    def create_widgets(self):
        vbox = QVBoxLayout()

        # Add label for the partition selection
        label = QLabel("What Partition do you want to flash?", self)
        
        label.setStyleSheet("font: 14pt Helvetica; margin-top: 20px; margin-bottom: 10px;")
        vbox.addWidget(label)

        # Add group box for the partition radiolist
        group_box = QGroupBox()
        group_box.setStyleSheet("font: 12pt Helvetica;")
        vbox.addWidget(group_box)

        hbox = QHBoxLayout()
        group_box.setLayout(hbox)
        
       
        # Add radiobuttons for each partition
        for i, partition in enumerate(self.partitions):
            rb = QRadioButton(partition)
            rb.setObjectName(partition)  # set object name to partition name
            hbox.addWidget(rb)
            if i == 0:
                rb.setChecked(True)

        # Add OK and Cancel buttons
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("font: 12pt Helvetica; margin-left: 20px; margin-right: 10px;")
        ok_button.clicked.connect(self.on_ok)
        hbox.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("font: 12pt Helvetica; margin-left: 10px; margin-right: 20px;")
        cancel_button.clicked.connect(self.on_cancel)
        hbox.addWidget(cancel_button)

        self.setLayout(vbox)

    def on_ok(self):
        for partition in self.partitions:
            rb = self.findChild(QRadioButton, partition)
            if rb and rb.isChecked():
                self.result = partition
                break
        self.accept()

    def on_cancel(self):
        self.result = None
        self.reject()


def select_partition(partitions):
    app = QApplication.instance() or QApplication([])
    dialog = PartitionDialog(partitions)
    result = dialog.exec()
    partition = dialog.result
    dialog.deleteLater()
    return partition


partitions = ["Boot", "Recovery", "Data", "System"]
partition = select_partition(partitions)

# Print selected Partition
if partition == 'Boot' or partition == 'Recovery' or partition == 'Data' or partition == 'System':
    print(f"{partition} selected")
else:
    print("Quiting....")
    sys.exit(0)

def select_img_file():
    app = QApplication.instance() or QApplication([])
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.ReadOnly
    file_filter = "IMG Files (*.img)"
    file_path, _ = QFileDialog.getOpenFileName(None, "Please select the *.IMG file to be flashed", os.path.expanduser("~"), file_filter, "", options=options)
    return file_path

part = ""
if partition == "Recovery":
    partition = "RECOVERY"
elif partition == "Boot":
    partition = "BOOT"
elif partition == "System":
    partition = "SYSTEM"
elif partition == "Data":
    partition = "DATA"
else:
    print("ERROR! - QUITING!")
    exit(0)

if __name__ == "__main__":
    partitions = ["Boot", "Recovery", "Data", "System"]
    img_file = select_img_file()
    if img_file == "":
        print("Quitting...")
        sys.exit(0)
    else:
        if operating_system == 'Windows':
            heimdallcmd = f"heimdall.exe flash --{partition} {img_file}"
            chdir = os.path.join(cwd, "heimdall")
            os.chdir(chdir)
        else:
            heimdallcmd = f"sudo heimdall flash --{partition} {img_file}"    
        heimdalloutput = os.system(heimdallcmd)
if str(heimdalloutput).find("ERROR: Failed to detect compatible download-mode device") != -1:
    print("Operation Completed Successfully!")
else:
    print("No Heimdall devices were detected!")
    app = QApplication.instance() or QApplication([])
    response = QMessageBox.question(None, "No Heimdall Devices Detected!", "No Heimdall devices detected! Do you want to restart the program?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if response == QMessageBox.Yes:
        restart()