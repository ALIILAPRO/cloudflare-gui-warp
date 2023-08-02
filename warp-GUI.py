import tkinter as tk
from tkinter import messagebox, Label
import os
import sys
import subprocess

version = "Beta 0.2"

window = tk.Tk()
window.title("CloudFlare GUI WARP " + version)
window.geometry("450x120")
window.eval('tk::PlaceWindow . center')
window.resizable(width=False, height=False)


def connect():
    os.system("warp-cli connect")
    messagebox.showinfo("Connected", "Successfully Connected to WARP.")
    connect_label.pack()
    disconnect_btn.pack()
    connect_btn.pack_forget()
    disconnect_label.pack_forget()

    update_data_label()


def disconnect():
    os.system("warp-cli disconnect")
    messagebox.showinfo("Disconnected", "Successfully Disconnected from WARP.")
    disconnect_label.pack()
    connect_btn.pack()
    disconnect_btn.pack_forget()
    connect_label.pack_forget()

    update_data_label()


def convert_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes = size_in_bytes / 1024
        unit_index += 1
    size_formatted = "{:.2f}".format(size_in_bytes)
    return size_formatted, units[unit_index]


def update_data_label():
    data_command = os.popen("warp-cli account").read()
    quota = 0
    premium_data = 0
    account_type = ""
    for line in data_command.splitlines():
        if "Quota" in line:
            quota = int(line.split(":")[1].strip())
        elif "Premium Data" in line:
            premium_data = int(line.split(":")[1].strip())
        elif "Account type" in line:
            account_type = line.split(":")[1].strip()

    quota_size, quota_unit = convert_size(quota)
    premium_data_size, premium_data_unit = convert_size(premium_data)

    accounttype_label.config(text=f"Account type: {account_type}")
    quota_label.config(text=f"Quota: {quota_size} {quota_unit}")
    used_data_label.config(text=f"Premium Data: {premium_data_size} {premium_data_unit}")


connect_btn = tk.Button(window, text="Connect", font=("Arial Bold", 15), bg="green", fg="white", command=connect)
connect_label = Label(window, text="Status update: Connected")
disconnect_btn = tk.Button(window, text="Disconnect", font=("Arial Bold", 15), bg="red", fg="white", command=disconnect)
disconnect_label = Label(window, text="Status update: Disconnected")

accounttype_label = Label(window, text="")
accounttype_label.pack()
quota_label = Label(window, text="")
quota_label.pack()
used_data_label = Label(window, text="")
used_data_label.pack()

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

command = os.popen("warp-cli status").read()
if "Connected" in command:
    connect_label.pack()
    disconnect_btn.pack()
if "Disconnected" in command:
    disconnect_label.pack()
    connect_btn.pack()

update_data_label()

window.mainloop()