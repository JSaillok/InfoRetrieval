import tkinter as tk
from tkinter import messagebox
from uploadgui import open_upload_window
from checkgui import open_check_window
from getDatagui import open_get_window

root = tk.Tk()
root.geometry("500x500")
root.title("Saillok Search")

def option_1():
    open_upload_window(root)

def option_2():
    open_check_window(root)

def option_3():
    open_get_window(root)


label = tk.Label(root, text="Welcome to the SaillokSearch!", font=('Arial', 18))
label.pack(padx=20, pady=10)

subtitle = tk.Label(root, text="Please select an option", font=('Arial', 12))
subtitle.pack(padx=20, pady=10)

var = tk.IntVar()
R1 = tk.Button(root, text="Upload to Elasticsearch", font=('Arial', 15), command=option_1,
               relief=tk.SUNKEN, borderwidth=2, bg="blue", fg="white", activebackground="cyan",
               activeforeground="black")
R1.pack(fill=tk.BOTH, expand=tk.YES)

R2 = tk.Button(root, text="Check through index name", font=('Arial', 15), command=option_2,
               relief=tk.SUNKEN, borderwidth=2, bg="blue", fg="white", activebackground="cyan",
               activeforeground="black")
R2.pack(fill=tk.BOTH, expand=tk.YES)

R3 = tk.Button(root, text="Search book", font=('Arial', 15), command=option_3,
               relief=tk.SUNKEN, borderwidth=2, bg="blue", fg="white", activebackground="cyan",
               activeforeground="black")
R3.pack(fill=tk.BOTH, expand=tk.YES)


def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?", icon="error"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

label = tk.Label(root, text="")
label.pack()

root.mainloop()