import tkinter as tk
from tkinter import messagebox
from checkIndex import checkdata

def open_check_window(root):
    check_window = tk.Toplevel(root)
    check_window.geometry("400x260")
    check_window.title("Check via Index")
    
    def check():
        index = index_name_entry.get()
        if not index:
            label_check.config(text="Error: Please fill index name!", fg="red")
        else:
            num_docs = checkdata(index)
            label_check.config(text=f"Index Existes!\nNumber of documents retrieved: {num_docs}", fg="green")

    index_name_label = tk.Label(check_window, text="Index Name:")
    index_name_label.pack(pady=10)
    index_name_entry = tk.Entry(check_window)
    index_name_entry.pack(pady=10)

    upload_button = tk.Button(check_window, text="Check", command=check)
    upload_button.pack(pady=10)

    label_check = tk.Label(check_window, text="")
    label_check.pack()