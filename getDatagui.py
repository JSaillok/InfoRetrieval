import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tabulate import tabulate
from closewin import close_windows
from getDataS import getdata
from getDataID import getdataisbnUid

def open_get_window(root):
    get_window = tk.Toplevel(root)
    get_window.geometry("400x260")
    get_window.title("Search with Keyword")

    def getbooks():
        keyword = keyword_entry.get()
        choice = messagebox.askquestion("Search Type", "Do you want search with User ID?", icon='question')
        if choice == "no":
            books = getdata('books', keyword)
            
            books_data = books.loc[:, ['book_title', 'book_author', 'score']]
            books_data_dict = books_data.to_dict(orient='records')
            table_style = 'grid'
            
            output_window = tk.Toplevel(root)
            output_window.title("Output")
        
            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 14, "bold"))
            style.configure("TText", font=("Helvetica", 12))
            style.configure("TButton", font=("Helvetica", 12), foreground="white", background="#007bff", padding=10)
        
            title_label = ttk.Label(output_window, text="MATCH QUERY METRIC", style="TLabel")    
            title_label.pack(pady=10)
        
            output_text = tk.Text(output_window, wrap="word", width=64, height=23)    
            output_text.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=5)
        
            table_str = tabulate(books_data_dict, headers='keys', tablefmt=table_style)
            output_text.insert(tk.END, table_str)
            output_text.config(state=tk.DISABLED)
        
            close_button = ttk.Button(output_window, text="Close", command=lambda: close_windows(output_window, get_window))    
            close_button.pack(pady=10)
        
            output_window.deiconify()
        else:
            get_window.attributes('-top', True)
            get_button.pack_forget()

            user_label = tk.Label(get_window, text="User ID:")
            user_label.pack(pady=10)
            user_entry = tk.Entry(get_window)
            user_entry.pack(pady=10)
            userId = user_entry.get()

            new_get_button = tk.Button(get_window, text="Let's goo", command=getbooks)
            new_get_button.pack(pady=10)
            
            booksUID = getdataisbnUid(keyword,userId,activate_nn = False)
            
    
    keyword_label = tk.Label(get_window, text="Keyword:")
    keyword_label.pack(pady=10)
    keyword_entry = tk.Entry(get_window)
    keyword_entry.pack(pady=10)

    get_button = tk.Button(get_window, text="Confirm", command=getbooks)
    get_button.pack(pady=10)

    label_get = tk.Label(get_window, text="")
    label_get.pack()