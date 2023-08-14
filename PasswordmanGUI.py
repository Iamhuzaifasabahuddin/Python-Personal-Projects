import time
import tkinter.ttk
import pwinput
import os
import tkinter as tk


# main funcs
def add(account, password, message_label, add_acc_entry, add_pwd_entry, toggle_add_fields, window):
    if account.strip() == "" or password.strip() == "":
        message_label.config(text="Account or Password cannot be empty", fg="red")
        message_label.pack()  # Make sure to pack the label even if the input is empty
    else:
        with open("NewPasswords.txt", 'a') as f:
            f.write(f"Account: {account}, Password: {password}\n")

        add_acc_entry.delete(0, tk.END)
        add_pwd_entry.delete(0, tk.END)

        toggle_add_fields()

        message_label.config(text="Account added successfully!", fg="green")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())


def view():
    return NotImplementedError


def edit():
    return NotImplementedError


def delete():
    return NotImplementedError


def upload():
    return NotImplementedError


def exist():
    return NotImplementedError


def master():
    return NotImplementedError



def gui():
    window = tk.Tk()
    window.title("Password manager")

    window.geometry("500x500")
    Tasks = ["add", "view", "edit", "delete", "upload", "search"]

    Task_label = tk.Label(window, text="Select your task:", font=("Lato", 20))
    items = tk.StringVar()
    Task_box = tk.ttk.Combobox(window, textvariable=items, font=("oswald", 20))

    Task_box["values"] = Tasks
    Task_box["state"] = 'readonly'

    add_acc_label = tk.Label(window, text="Enter your account: ")
    add_pwd_label = tk.Label(window, text="Enter your password: ")
    add_acc_entry = tk.Entry(window, font=("oswald", 20))
    add_acc_entry.bind('<Return>', )
    add_pwd_entry = tk.Entry(window, font=("oswald", 20), show="*")
    add_message_label = tk.Label(window, text="", font=("oswald", 14))
    add_button = tk.Button(window, text="Add Account", command=lambda: add(add_acc_entry.get(), add_pwd_entry.get(),
                                                                           add_message_label, add_acc_entry,
                                                                           add_pwd_entry,
                                                                           toggle_add_fields, window),
                           font=("oswald", 20))
    add_acc_entry.bind("<Return>", lambda event: add(add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry, toggle_add_fields,
                                                     window))
    add_pwd_entry.bind("<Return>", lambda event: add(add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry, toggle_add_fields,
                                                     window))

    def toggle_add_fields():
            add_acc_label.pack_forget()
            add_acc_entry.pack_forget()
            add_pwd_label.pack_forget()
            add_pwd_entry.pack_forget()
            add_button.pack_forget()

    def get_value(event):
        """Return the value from the combobox"""
        selected_value = items.get()

        if selected_value == "add":
            add_acc_label.pack()
            add_acc_entry.pack()
            add_pwd_label.pack()
            add_pwd_entry.pack()
            add_button.pack()
        elif selected_value == "view":
            master()
            view()
        elif selected_value == "search":
            exist()
        elif selected_value == "delete":
            delete()
        elif selected_value == "edit":
            edit()
        elif selected_value == "upload":
            upload()
        else:
            return "Select a value from the dropdown list"

    Task_box.bind('<<ComboboxSelected>>', get_value)
    Task_label.pack()
    Task_box.pack()

    window.mainloop()


if __name__ == '__main__':
    gui()
