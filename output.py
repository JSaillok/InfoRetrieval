import tkinter as tk
from tkinter import ttk
from closewin import close_windows

def output(root,books,get_window):           
    output_window = tk.Toplevel(root)
    output_window.title("Output")

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 14, "bold"))
    style.configure("TText", font=("Helvetica", 12))

    title_label = ttk.Label(output_window, text="MATCH QUERY METRIC", style="TLabel")    
    title_label.pack(pady=10)

    output_text = tk.Text(output_window, wrap="word", width=80, height=20)    
    output_text.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=5)

    output_text.insert(tk.END, str(books.loc[:, ['book_title', 'book_author', 'score']]))    
    output_text.config(state=tk.DISABLED)

    close_button = ttk.Button(output_window, text="Close", command=lambda: close_windows(output_window, get_window))    
    close_button.pack(pady=10)

    output_window.deiconify()