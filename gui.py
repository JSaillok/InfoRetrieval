from tkinter import *
from upload import uploadData
from checkIndex import checkdata
from getDataS import getdata
from getDataID import getdataisbnUid

#Initialize the main window
root = Tk()
root.geometry("400x250")
root.title("Saillok Search")

def option_1():
    fname = input("Give the name of File: ")
    iname = input("Give the index of File: ")
    uploadData(fname, iname)
    label.config(text="Upload Completed!")

def option_2():
    iname = input("Give the index of File you are searching: ")
    checkdata(iname)
    label.config(text="Index Checked!")

def option_3():
    keyword = input("Give the keyword: ")
    print("1. Search with simply metric")
    print("2. Search with uid metric")
    choice = int(input("Choice: "))
    if choice == 1:
        books = getdata('books', keyword)
        output = 'MATCH QUERY METRIC\n'
        output += str(books.loc[:, ['book_title', 'book_author', 'score']])
    elif choice == 2:
        user = int(input("Give user id: "))
        ch = input("Use neural network? [Y/n]: ").lower().strip()
        if ch == 'y':
            state = True
        else:
            state = False
        books = getdataisbnUid(keyword, user, activate_nn=state)
        output = 'MATCH QUERY METRIC THROUGH USER ID\n'
        output += str(books.loc[:, ['book_title', 'book_author', 'score']])
    label.config(text=output)

def sel():
    choice = var.get()
    if choice == 1:
        option_1()
    elif choice == 2:
        option_2()
    elif choice == 3:
        option_3()

label = Label(root, text="Welcome!", font=('Helvetica', 18))
label.pack(padx=20, pady=20)

var = IntVar()
R1 = Radiobutton(root, text="Upload to Elasticsearch", variable=var, value=1, command=sel)
R1.pack(anchor=W)

R2 = Radiobutton(root, text="Check through index name", variable=var, value=2, command=sel)
R2.pack(anchor=W)

R3 = Radiobutton(root, text="Search book", variable=var, value=3, command=sel)
R3.pack(anchor=W)

ConButton = Button(root, text='Continue')
ConButton.pack()

label = Label(root, text="")
label.pack()

root.mainloop()
