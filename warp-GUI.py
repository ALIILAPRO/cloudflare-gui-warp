

import tkinter as tk 
from tkinter import messagebox, Label
import os 
import sys
import subprocess

version = "Beta 0.1"
  
window = tk.Tk() 
window.title("CloudFlare GUI WARP " + version) 
window.geometry("450x75")
window.eval('tk::PlaceWindow . center')
window.resizable(width=False, height=False)

def connect():     
    os.system("warp-cli connect")     
    messagebox.showinfo("Connected", "Successfully Connected to WARP.")
    connect_label.pack()
    disconnect_btn.pack()
    connect_btn.pack_forget()
    disconnect_label.pack_forget()
def disconnect():     
    os.system("warp-cli disconnect")     
    messagebox.showinfo("Disconnected", "Successfully Disconnected from WARP.")
    disconnect_label.pack()
    connect_btn.pack()
    disconnect_btn.pack_forget()
    connect_label.pack_forget()

connect_btn = tk.Button(window, text ="Connect",font = ("Arial Bold", 15), bg = "green", fg = "white", command = connect)
connect_label = Label(window, text="Status update: Connected") 
disconnect_btn = tk.Button(window, text ="Disconnect",font = ("Arial Bold", 15), bg = "red", fg = "white", command = disconnect)
disconnect_label = Label(window, text="Status update: DisConnected")    

if sys.platform != "linux":
    messagebox.showerror("Error", "This only runs on Linux!")
    sys.exit()

if sys.version_info.major < 3:
    messagebox.showerror("Error", "This requires Python 3 or above!")
    sys.exit()

daemon = subprocess.call(['systemctl', 'is-active', '--quiet', 'warp-svc'])
if daemon != 0:
    messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run")
    sys.exit()

command= os.popen("warp-cli status").read()
if "Connected" in command: 
    connect_label.pack()
    disconnect_btn.pack()
if "Disconnected" in command:
    disconnect_label.pack()
    connect_btn.pack()          
  
window.mainloop()