import tkinter as tk
import tkinter.ttk
import sqlite3


# main funcs
def add(username, account, password, message_label, add_acc_entry, add_pwd_entry, toggle_add_fields, window):
    selected_account_value = username()
    if selected_account_value.strip() == "" or account.strip() == "" or password.strip() == "":
        message_label.config(text="Username or Account or Password cannot be empty", fg="red")
        message_label.pack()
    else:
        connection = sqlite3.connect('Passwords.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO manager VALUES(?, ?, ?)", (selected_account_value, account, password))
        connection.commit()

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

    main_label = tk.Label(text="Welcome to the Password Manager")


    # Main taskbox for adding
    Tasks = ["Options", "add", "view", "edit", "delete", "upload", "search"]
    Task_label = tk.Label(window, text="Select your task:", font=("Lato", 20))
    items = tk.StringVar()
    Task_box = tk.ttk.Combobox(window, textvariable=items, font=("oswald", 20))
    Task_box["values"] = Tasks
    Task_box["state"] = 'readonly'

    # Accounts adding taskbox
    Accounts = ["Facebook", "X", "Instagram", "Gmail", "LinkedIn", "Github", "Hotmail", "University", "Other"]
    add_user_label = tk.Label(window, text="Select account to add: ")
    accounts = tk.StringVar()
    Accounts_box = tk.ttk.Combobox(window, textvariable=accounts, font=("oswald", 20))
    Accounts_box["values"] = Accounts
    Accounts_box["state"] = 'readonly'

    def selected_account(event=None):
        if accounts.get() == "Other":
            add_user_label.config(text="Enter account: ")
            Accounts_box.config(state='normal')  # Allow editing the combobox
        else:
            Accounts_box.config(state='readonly')  # Disable editing

        return accounts.get()

    Accounts_box.bind('<<ComboboxSelected>>', selected_account)

    add_user_label = tk.Label(window, text="Add service account to add: ")
    add_acc_label = tk.Label(window, text="Enter your account: ")
    add_pwd_label = tk.Label(window, text="Enter your password: ")
    add_acc_entry = tk.Entry(window, font=("oswald", 20))
    add_pwd_entry = tk.Entry(window, font=("oswald", 20), show="*")
    add_message_label = tk.Label(window, text="", font=("oswald", 14))
    add_button = tk.Button(window, text="Add Account",
                           command=lambda: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                               add_message_label, add_acc_entry,
                                               add_pwd_entry, toggle_add_fields, window),
                           font=("oswald", 20))

    def reset_taskbox():
        Task_box.set(Tasks[0])

    def toggle_add_fields():
        add_acc_label.pack_forget()
        add_acc_entry.pack_forget()
        add_pwd_label.pack_forget()
        add_pwd_entry.pack_forget()
        add_user_label.pack_forget()  # Hide the label for adding a new account
        Accounts_box.pack_forget()
        add_button.pack_forget()
        reset_taskbox()

    def get_value(event):
        """Return the value from the combobox"""
        selected_value = items.get()

        main_label.pack_forget()  # Hide the main label by default

        if selected_value == "Options":
            main_label.config(text="Please select an action!", fg="red")
            main_label.pack()  # Show the main label when "Options" is selected
        elif selected_value == "add":
            add_user_label.pack()
            Accounts_box.pack()
            add_acc_label.pack()
            add_acc_entry.pack()
            add_pwd_label.pack()
            add_pwd_entry.pack()
            selected_account()  # Call the selected_account function to handle the editing of Accounts_box
            add_button.pack()
        else:
            toggle_add_fields()
            if selected_value == "view":
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

    # Bind the Return key to the entry fields and button
    add_acc_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry,
                                                     toggle_add_fields,
                                                     window))
    add_pwd_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry,
                                                     toggle_add_fields,
                                                     window))
    add_button.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                  add_message_label, add_acc_entry, add_pwd_entry,
                                                  toggle_add_fields,
                                                  window))

    window.mainloop()


if __name__ == '__main__':
    gui()
