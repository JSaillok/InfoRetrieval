import tkinter as tk
from tkinter import messagebox
from upload import uploadData

def open_upload_window(root):
    upload_window = tk.Toplevel(root)
    upload_window.geometry("400x260")
    upload_window.title("Upload to Elasticsearch")

    def upload():
        fname = file_name_entry.get()
        iname = index_name_entry.get()
        if not fname or not iname:
            label_upload.config(text="Error: Please enter both file name and index name!", fg="red")
        else:  
            try:    
                uploadData(fname, iname)
                label_upload.config(text="Upload Completed!", fg="green")
            except FileNotFoundError:
                label_upload.config(text="File not found!", fg="red")
            except Exception as e:
                label_upload.config(text=f"Error: {str(e)}", fg="red")


    file_name_label = tk.Label(upload_window, text="File Name:")
    file_name_label.pack(pady=10)
    file_name_entry = tk.Entry(upload_window)
    file_name_entry.pack(pady=10)

    index_name_label = tk.Label(upload_window, text="Index Name:")
    index_name_label.pack(pady=10)
    index_name_entry = tk.Entry(upload_window)
    index_name_entry.pack(pady=10)

    upload_button = tk.Button(upload_window, text="Upload", command=upload)
    upload_button.pack(pady=10)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            upload_window.destroy()

    upload_window.protocol("WM_DELETE_WINDOW", on_closing)

    label_upload = tk.Label(upload_window, text="")
    label_upload.pack()