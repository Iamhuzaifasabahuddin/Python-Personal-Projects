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
        cursor.execute("INSERT INTO manager VALUES(?, ?, ?)", (selected_account_value.title(),
                                                               account.title(), password))
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


def exist(username, message_label, toggle_search, window):
    if username.strip() == "":
        message_label.config(text="Please enter an account! ", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())
    else:
        connection = sqlite3.connect("Passwords.db")
        cursor = connection.cursor()
        res = cursor.execute("SELECT USERNAME, ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (username.title(),))
        result = res.fetchall()
        if not result:
            message_label.config(text="Account doesnt exist", fg="red")
            message_label.pack()
            toggle_search(False)
            window.after(2000, lambda: message_label.pack_forget())
        else:
            message_label.config(text=f"ACCOUNT EXIST \n ACCOUNT: {result[0][0]} \n USERNAME: {result[0][1]} "
                                      f"\n PASSWORD: {result[0][2]}", fg="green")
            message_label.pack()
            toggle_search(False)
            window.after(2000, lambda: message_label.pack_forget())


def master(password, message_label, master_entry, option, toggle_master, toggle_search, window):
    with open("master.txt", "r") as file:
        master_password = file.readline().strip()
    if password.strip() == "":
        message_label.config(text="Please enter your password!", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())
    else:
        if password == master_password:
            message_label.config(text="Authorization successful", fg="green")
            message_label.pack()
            master_entry.delete(0, tk.END)
            toggle_master()
            if option == "search":
                toggle_search(True)
            elif option == "view":
                raise NotImplementedError
            window.after(2000, lambda: message_label.pack_forget())
        else:
            message_label.config(text="Authorization failed", fg="red")
            message_label.pack()
            master_entry.delete(0, tk.END)
            toggle_search(False)
            window.after(2000, lambda: message_label.pack_forget())


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

    master_label = tk.Label(window, text="Enter Master Password: ")
    master_entry = tk.Entry(window, font=("oswald", 20), show="*")
    master_main_label = tk.Label(window, text="", font=("oswald", 14))
    master_button = tk.Button(window, text="Check",
                              command=lambda: master(master_entry.get(), master_main_label, master_entry, toggle_master,
                                                     items,
                                                     toggle_search, window), font=("oswald", 20))

    search_label = tk.Label(window, text="Enter Account To Search: ")
    search_entry = tk.Entry(window, font=("oswald", 20))
    search_main_label = tk.Label(window, text="", font=("oswald", 14))
    search_button = tk.Button(window, text="Search",
                              command=lambda: exist(search_entry.get(), search_main_label, toggle_search, window))

    def reset():
        Task_box.set(Tasks[0])
    # Used to unpack all add fields
    def toggle_add_fields():
        """Unpacks all add fields"""
        add_acc_label.pack_forget()
        add_acc_entry.pack_forget()
        add_pwd_label.pack_forget()
        add_pwd_entry.pack_forget()
        add_user_label.pack_forget()  # Hide the label for adding a new account
        Accounts_box.pack_forget()
        add_button.pack_forget()

    def toggle_master():
        """Unpacks all master"""
        master_entry.pack_forget()
        master_label.pack_forget()
        master_button.pack_forget()

    def toggle_search(enable):
        if enable:
            search_label.pack()
            search_entry.pack()
            search_button.pack()
        else:
            search_label.pack_forget()
            search_entry.pack_forget()
            search_button.pack_forget()

    # Used to get the value from the main combobox
    def get_value(event=None):
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
                view()
            elif selected_value == "search":
                master_label.pack()
                master_entry.pack()
                master_button.pack()
                toggle_search(False)
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

    # Add Bindings
    add_acc_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry,
                                                     toggle_add_fields,
                                                     window))
    add_pwd_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, add_acc_entry, add_pwd_entry,
                                                     toggle_add_fields,
                                                     window))
    add_button.config(command=lambda: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                          add_message_label, add_acc_entry, add_pwd_entry,
                                          toggle_add_fields,
                                          window))
    # Master Bindings
    master_entry.bind("<Return>", lambda event: master(master_entry.get(), master_main_label, master_entry,
                                                       items.get(), toggle_master, toggle_search, window))
    master_button.config(command=lambda: master(master_entry.get(), master_main_label, master_entry,
                                                items.get(), toggle_master, toggle_search, window))
    # Search binding
    search_entry.bind("<Return>", lambda event: exist(search_entry.get(), search_main_label, toggle_search, window))
    search_button.config(command=lambda: exist(search_entry.get(), search_main_label, toggle_search, window))

    window.mainloop()


if __name__ == '__main__':
    gui()
