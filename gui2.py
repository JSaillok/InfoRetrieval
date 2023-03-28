from tkinter import *

class MainMenu:
    def __init__(self, master):
        self.master = master
        master.title("Saillok Search")

        label = Label(root, text="Welcome!", font=('Helvetica', 18))
        label.pack(padx=20, pady=20)

        self.choice = IntVar()
        self.choice.set(1)

        self.upload_radio = Radiobutton(master, text="Upload File", variable=self.choice, value=1)
        self.upload_radio.pack()

        self.check_radio = Radiobutton(master, text="Check Index", variable=self.choice, value=2)
        self.check_radio.pack()

        self.retrieve_radio = Radiobutton(master, text="Retrieve Data", variable=self.choice, value=3)
        self.retrieve_radio.pack()

        self.confirm_button = Button(master, text="Confirm", command=self.confirm_choice)
        self.confirm_button.pack()

    def confirm_choice(self):
        choice = self.choice.get()
        if choice == 1:
            self.upload_screen()
        elif choice == 2:
            self.check_screen()
        elif choice == 3:
            self.retrieve_screen()

    def upload_screen(self):
        self.upload_window = Toplevel(self.master)
        self.upload_window.title("Upload File")

        fname_label = Label(self.upload_window, text="Enter file name:")
        fname_label.pack()

        self.fname_entry = Entry(self.upload_window)
        self.fname_entry.pack()

        iname_label = Label(self.upload_window, text="Enter index name:")
        iname_label.pack()

        self.iname_entry = Entry(self.upload_window)
        self.iname_entry.pack()

        upload_button = Button(self.upload_window, text="Upload", command=self.upload_file)
        upload_button.pack()

    def check_screen(self):
        # code for check screen
        pass

    def retrieve_screen(self):
        # code for retrieve screen
        pass

root = Tk()
root.geometry("400x250")
main_menu = MainMenu(root)
root.mainloop()
