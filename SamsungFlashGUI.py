import os
import platform
import shutil
import sys

from PySide2.QtWidgets import QApplication, QDialog, QFileDialog, QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLabel, QMessageBox

cwd = os.path.dirname(os.path.abspath(__file__))
operating_system = platform.system()
temp = os.path.join(cwd, "temp")
if os.path.exists(temp):
    print("Removing Temporary Directory...")
    shutil.rmtree(temp)

if operating_system == 'Linux':
    print("You are running Linux!")
elif operating_system == 'Windows':
    print("You are running Windows")
else:
    print("Unsupported operating system:", operating_system)


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
    result = dialog.exec_()
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


if __name__ == "__main__":
    partitions = ["Boot", "Recovery", "Data", "System"]

    # Print selected Partition
    if partition == 'Boot' or partition == 'Recovery' or partition == 'Data' or partition == 'System':
        print(f"{partition} selected")
    else:
        print("Quiting....")
        sys.exit(0)

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
    app = QApplication.instance() or QApplication([])
    msg_box = QMessageBox(QMessageBox.Critical, "Error", "Failed to detect compatible download-mode device", QMessageBox.Ok)
    msg_box.exec_()