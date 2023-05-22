import tkinter as tk
import os
import platform
import  ttkbootstrap as ttk
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
import sys
global part
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
cwd = os.path.dirname(os.path.abspath(__file__))
operating_system = platform.system()
def file():
	global file
	filetypes = (
        ('Image Files', '*.img'),
        ('All files', '*.*')
    )
	file = askopenfilename(filetypes =filetypes)
	flash.configure(state="normal")
	print(file)
def flash():
    global part
    global file
    if operating_system == 'Windows':
        heimdallcmd = f"heimdall.exe flash --{part} {file}"
        chdir = os.path.join(cwd, "heimdall")
        os.chdir(chdir)
    else:
        heimdallcmd = f"heimdall flash --{part} {file}"    
        print(f"Executing command: {heimdallcmd}")
        heimdalloutput = os.system(heimdallcmd)
        if str(heimdalloutput).find("ERROR: Failed to detect compatible download-mode device") != 1:
        	response = messagebox.askquestion("No Heimdall Devices Detected!", "No Heimdall devices detected! Do you want to restart the program?")
        	if response == 'yes':
        		restart()
        	else:
        		exit()




def boott():
	global part
	part = 'BOOT'
def datat():
	global part
	part = 'DATA'
def systemr():
	global part
	part = 'SYSTEM'
def recoveryt():
	global part
	part = 'RECOVERY'
operating_system = platform.system()
if operating_system == 'Linux':
    print("You are running Linux!")
elif operating_system == 'Windows':
    print("You are running Windows")
else:
    print("Unsupported operating system:", operating_system)
    exit()
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
cwd = os.path.dirname(os.path.abspath(__file__))
# create a window 
window = ttk.Window(themename = 'darkly')
window.title('SamsungFlashGUI')
window.geometry('800x200')
label = ttk.Label(window , text = 'Please select the Partition / File you would like to flash')
label.pack()
recovery = ttk.Radiobutton(window , text = 'Recovery' , value = 4 ,command = recoveryt )
recovery.place(x=0, y=160)
boot = ttk.Radiobutton(window , text = 'Boot' , value = 3 , command = boott )
boot.place(x=0, y=40)
system = ttk.Radiobutton(window , text = 'System' , value = 1 , command = systemr )
system.place(x=0, y=80)
data = ttk.Radiobutton(window , text = 'Data' , value = 2 , command = datat )
file_select = ttk.Button(window , text = 'Select a File' , command = file )
file_select.place(x=220 , y=100)
data.place(x=0, y=120)
flash = ttk.Button(window , text = 'FLASH!' , command = flash)
flash.place(x=460 , y=100)
flash.configure(state="disabled")
# run 
window.mainloop()
