# Only made possible by Heimdall
import customtkinter
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename
import os
import sys
import platform
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
cwd = os.path.dirname(os.path.abspath(__file__))
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

def boot():
	global part
	part = 'BOOT'
def data():
	global part
	part = 'DATA'
def system():
	global part
	part = 'SYSTEM'
def recovery():
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
def file():
	global file
	filetypes = (
        ('Image Files', '*.img'),
        ('All files', '*.*')
    )
	file = askopenfilename(filetypes =filetypes)
	flash.configure(state="normal")
	print(file)
app = customtkinter.CTk()
app.title("Samsung Flash GUI")
app.geometry("450x200")
label = customtkinter.CTkLabel(app , text = 'Please select the Partition / File you would like to flash' , font =("Poppins" , 15) )
label.place(x=60 , y=0)
button = customtkinter.CTkButton(app, text="Select a File", command=file)
button.grid(row=0, column=0 , padx=160, pady=50 )
var1 = customtkinter.StringVar()
recovery = customtkinter.CTkRadioButton(app , text = 'Recovery' , value = 1 ,command = recovery , variable = var1)
recovery.place(x=0, y=160)
boot = customtkinter.CTkRadioButton(app , text = 'Boot' , value = 1 , command = boot , variable = var1)
boot.place(x=0, y=40)
system = customtkinter.CTkRadioButton(app , text = 'System' , value = 1 , command = system , variable = var1)
system.place(x=0, y=80)
data = customtkinter.CTkRadioButton(app , text = 'Data' , value = 1 , command = data, variable = var1)
flash = customtkinter.CTkButton(app , text = 'FLASH!' , command = flash)
flash.place(x=160,y=100)
flash.configure(state="disabled")
data.place(x=0, y=120)
app.mainloop()