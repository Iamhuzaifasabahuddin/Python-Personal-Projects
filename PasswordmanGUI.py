import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3
import os
import logging

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

current_selection = None


# main funcs
def show_message(message_label, text, color, duration=2000):
    """
       Display a message on the GUI.

       Args:
           message_label (tk.Label): The label widget to display the message.
           text (str): The message text.
           color (str): The color of the message text.
           duration (int, optional): Duration in milliseconds to display the message. Default is 2000ms.
       """
    message_label.config(text=text, fg=color)
    message_label.pack()
    message_label.after(duration, lambda: message_label.pack_forget())
    logging.info(text)


def add(username, account, password, message_label, toggle_add_fields):
    """
       Add an account to the database.

       Args:
           username (function): Function to get the selected account value.
           account (str): Account name.
           password (str): Account password.
           message_label (tk.Label): The label to display messages.
           toggle_add_fields (function): Function to toggle add fields visibility.
       """
    selected_account_value = username()
    if selected_account_value.strip() == "" or account.strip() == "" or password.strip() == "":
        show_message(message_label, "Username or Account or Password cannot be empty", "red")
    else:
        connection = sqlite3.connect('Passwords.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO manager VALUES(?, ?, ?)", (selected_account_value.title(),
                                                               account.title(), password))
        connection.commit()
        toggle_add_fields(False)
        show_message(message_label, "Account added successfully!", "green")


def view():
    return NotImplementedError


def edit(search, account, username, password, message_label, edit_search, toggle_edit):
    """
       Edit an existing account's details.

       Args:
           search (str): Account username to search for.
           account (str): New account name.
           username (str): New username.
           password (str): New password.
           message_label (tk.Label): The label to display messages.
           edit_search (tk.Entry): The entry widget for searching.
           toggle_edit (function): Function to toggle edit fields visibility.
       """
    if search.strip() == "" or account.strip() == "" or username.strip() == "" or password.strip() == "":
        show_message(message_label, "Fields Cannot Be Empty", "red")
        return
    connection = sqlite3.connect("Passwords.db")
    cursor = connection.cursor()

    result = cursor.execute("SELECT USERNAME, ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (search,))

    existing_data = result.fetchone()
    if not existing_data:
        show_message(message_label, "Account not found", "red")
        edit_search.delete(0, tk.END)
    else:
        new_account = account.strip() if account.strip() else existing_data[1]
        new_username = username.strip() if username.strip() else existing_data[0]
        new_password = password.strip() if password.strip() else existing_data[2]

        cursor.execute("UPDATE manager SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE USERNAME=?",
                       (new_account.title(), new_username.title(), new_password, search))
        connection.commit()
        toggle_edit(False)
        show_message(message_label, "Account updated", "green")
    connection.close()


def delete(Account, message_label, toggle_delete):
    if Account.strip() == "":
        show_message(message_label, "Please Enter An Account", "red")
        return  # Return to prevent further execution of the function

    connection = sqlite3.connect('Passwords.db')
    cursor = connection.cursor()
    results = cursor.execute("SELECT USERNAME,ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (Account.title(),))
    results = results.fetchall()

    if not results:
        show_message(message_label, "Account does not exist!", "red")
        toggle_delete(False)
    else:
        cursor.execute("DELETE FROM manager WHERE USERNAME=?", (Account.strip().title(),))
        connection.commit()
        toggle_delete(False)
        show_message(message_label, "Account deleted", "green")
    connection.close()


def upload(message_label, toggle_upload):
    """
        Upload the database file to Google Drive.

        This function uploads the database file to a designated folder in Google Drive
        after validating a provided passcode.

        Args:
            message_label (tk.Label): The label widget to display messages.
            toggle_upload (function): Function to toggle upload fields visibility.
    """
    toggle_upload(False)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json'):
        creds = Credentials.from_authorized_user_file(
            r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Drive_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        response = service.files().list(
            q="name='Hexzdrivefolder' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive').execute()

        if not response['files']:
            file_metadata = {
                "name": "Hexzdrivefolder",
                "mimeType": "application/vnd.google-apps.folder",
            }

            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        file_metadata = {
            "name": "MyPasswords.db",
            "parents": [folder_id]
        }

        file_path = r"C:\Users\huzai\PycharmProjects\Python-projects-1\Passwords.db"
        # Search for the existing file in Google Drive
        existing_file = service.files().list(
            q=f"name='MyPasswords.db' and parents='{folder_id}'",
            spaces='drive').execute()

        if existing_file['files']:
            existing_file_id = existing_file['files'][0]['id']

            media = MediaFileUpload(file_path, resumable=True)
            update_file = service.files().update(fileId=existing_file_id, media_body=media).execute()

            logging.info(f"Updated file: {update_file.get('name')}")
            show_message(message_label, "File Updated Successfully", "green")
        else:
            media = MediaFileUpload(file_path)
            upload_file = service.files().create(body=file_metadata, media_body=media).execute()
            logging.info(f"Uploaded file: {upload_file.get('name')}")
            show_message(message_label, "File Uploaded To Google Drive", "green")
    except HttpError as error:
        logging.info(f'An error occurred: {error}')
        show_message(message_label, "An error occurred during upload", "red")


def exist(username, message_label, toggle_search, search_listbox):
    """
        Check if an account exists in the database.

        This function queries the database to determine if the provided account username exists.
        It displays the account details if found, or a message if the account does not exist.

        Args:
            username (str): The account username to search for.
            message_label (tk.Label): The label widget to display messages.
            toggle_search (function): Function to toggle search fields visibility.
            search_listbox(tk.ListBox): Creates a Taskbox which is also scrollable
    """
    if username.strip() == "":
        show_message(message_label, "Please enter an account! ", "red")
    else:
        connection = sqlite3.connect("Passwords.db")
        cursor = connection.cursor()
        res = cursor.execute("SELECT USERNAME, ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (username.title(),))
        result = res.fetchall()
        if not result:
            toggle_search(False)
            show_message(message_label, "Account doesnt exist", "red")
        else:
            show_message(message_label,"Showing Account / Accounts", "green")
            for index, values in enumerate(result, start=1):
                search_listbox.insert(tk.END, f"Account {index}\n\n")  # We insert from END due to it adds from where
                # it left off
                search_listbox.insert(tk.END, f"ACCOUNT: {values[0]}\nUSERNAME: {values[1]}\nPASSWORD: {values[2]}\n\n")
            search_listbox.pack()  # Display the scrolled text widget
            toggle_search(False)


def master(password, message_label, master_entry, option, toggle_master, toggle_search, toggle_upload):
    """
       Validate the master password and perform corresponding actions.

       This function checks if the provided password matches the stored master password.
       If the password is correct, it performs actions based on the selected option, such as
       toggling search fields for account existence checking.

       Args:
           password (str): The password input provided by the user.
           message_label (tk.Label): The label widget to display messages.
           master_entry (tk.Entry): The entry widget for master password input.
           option (str): The selected option ("search" or "view") for performing actions.
           toggle_master (function): Function to toggle master fields visibility.
           toggle_search (function): Function to toggle search fields visibility.
    """
    with open("master.txt", "r") as file:
        master_password = file.readline().strip()
    if password.strip() == "":
        show_message(message_label, "Please enter your password!", "red")
    else:
        if password == master_password:
            master_entry.delete(0, tk.END)
            toggle_master(False)
            show_message(message_label, "Authorization successful", "green")
            if option == "search":
                toggle_search(True)
            elif option == "view":
                show_message(message_label, "Unavailable", "red")
            elif option == "upload":
                toggle_upload(True)
        else:
            master_entry.delete(0, tk.END)
            toggle_search(False)
            show_message(message_label, "Authorization failed", "red")


def gui():
    """
        Create and manage the graphical user interface for the password manager.

        This function initializes the main application window and sets up various GUI elements,
        such as labels, comboboxes, entry fields, and buttons. It handles user interaction,
        manages the visibility of different sections, and delegates tasks to other functions.
    """
    window = tk.Tk()
    window.title("Password manager")
    window.geometry("600x600")
    icon = tk.PhotoImage(file="password.png")
    window.iconphoto(True, icon)

    # Main Label
    main_label = tk.Label(text="Welcome To The Password Manager", font=("Lato", 20))
    main_label.pack(pady=5)

    # Main taskbox for adding
    Tasks = ["Options", "add", "view", "edit", "delete", "upload", "search"]
    Task_label = tk.Label(window, text="Select your task:", font=("Lato", 15))
    items = tk.StringVar()
    Task_box = tk.ttk.Combobox(window, textvariable=items, font=("oswald", 20))
    Task_box["values"] = Tasks
    Task_box["state"] = 'readonly'

    # Accounts adding ComboBox
    Accounts = [" ", "Facebook", "X", "Instagram", "Gmail", "LinkedIn", "Github", "Hotmail", "University", "Other"]
    add_user_label = tk.Label(window, text="Select account to add: ")
    accounts = tk.StringVar()
    Accounts_box = tk.ttk.Combobox(window, textvariable=accounts, font=("oswald", 20))
    Accounts_box["values"] = Accounts
    Accounts_box["state"] = 'readonly'

    def selected_account(event=None):
        """Edits the state of the account combobox"""
        if accounts.get() == "Other":
            add_user_label.config(text="Enter account: ")
            Accounts_box.config(state='normal')  # Allow editing the combobox
        else:
            Accounts_box.config(state='readonly')  # Disable editing
        return accounts.get()

    Accounts_box.bind('<<ComboboxSelected>>', selected_account)

    # Add Function Fields
    add_user_label = tk.Label(window, text="Add service account to add: ", font=("oswald", 10))
    add_acc_label = tk.Label(window, text="Enter your account: ", font=("oswald", 10))
    add_pwd_label = tk.Label(window, text="Enter your password: ", font=("oswald", 10))
    add_user_label = tk.Label(window, text="Select account to add: ")
    add_acc_label = tk.Label(window, text="Enter your account/Username: ")
    add_pwd_label = tk.Label(window, text="Enter your password: ")
    add_acc_entry = tk.Entry(window, font=("oswald", 20))
    add_pwd_entry = tk.Entry(window, font=("oswald", 20), show="*")
    add_message_label = tk.Label(window, text="", font=("oswald", 14))
    add_button = tk.Button(window, text="Add Account",
                           command=lambda: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                               add_message_label, toggle_add_fields),
                           font=("oswald", 20))

    # Master Function Fields
    master_label = tk.Label(window, text="Enter Master Password: ", font=("oswald", 10))
    master_entry = tk.Entry(window, font=("oswald", 20), show="*")
    master_main_label = tk.Label(window, text="", font=("oswald", 14))
    master_button = tk.Button(window, text="Check",
                              command=lambda: master(master_entry.get(), master_main_label, master_entry, items.get(),
                                                     toggle_master,

                                                     toggle_search, toggle_upload), font=("oswald", 20))

    # Search Function Fields
    search_label = tk.Label(window, text="Enter Account To Search: ", font=("oswald", 10))
    search_entry = tk.Entry(window, font=("oswald", 20))
    search_main_label = tk.Label(window, text="", font=("oswald", 14))
    search_listbox = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=20, font=("oswald", 14))
    search_button = tk.Button(window, text="Search",
                              command=lambda: exist(search_entry.get(), search_main_label, toggle_search,
                                                    search_listbox),
                              font=("oswald", 20))

    # Edit Function Fields
    edit_label = tk.Label(window, text="Enter Account To Edit: ", font=("oswald", 10))
    edit_search = tk.Entry(window, font=("oswald", 20))
    edit_label_user = tk.Label(window, text="Enter Updated Account: ", font=("oswald", 10))
    edit_entry_username = tk.Entry(window, font=("oswald", 20))
    edit_label_acc = tk.Label(window, text="Enter Updated Username: ", font=("oswald", 10))
    edit_entry_account = tk.Entry(window, font=("oswald", 20))
    edit_label_pass = tk.Label(window, text="Enter Updated Password: ", font=("oswald", 10))
    edit_entry_password = tk.Entry(window, font=("oswald", 20), show="*")
    edit_main_label = tk.Label(window, text="", font=("oswald", 14))
    edit_button = tk.Button(window, text="Edit",
                            command=lambda: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                                 edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                                 ), font=("oswald", 20))

    # Delete Function Fields
    delete_main_label = tk.Label(window, text="", font=("oswald", 14))
    delete_entry_label = tk.Label(window, text="Enter Account to Be Deleted: ", font=("oswald", 10))
    delete_entry = tk.Entry(window, font=("oswald", 20))
    delete_Button = tk.Button(window, text="Delete", command=lambda: delete(delete_entry.get(), delete_main_label,
                                                                            toggle_delete), font=("oswald", 20))

    # Upload Function Fields
    upload_label = tk.Label(window, text="Enter to Upload: ", font=("oswald", 10))
    upload_main_label = tk.Label(window, text="", font=("oswald", 14))
    upload_button = tk.Button(window, text="Upload", command=lambda: upload(upload_main_label, toggle_upload))

    def reset():
        """ Resets the main combobox to index 0."""
        Task_box.set(Tasks[0])

    # Used to unpack all add fields
    def toggle_add_fields(enable):
        """Packs and Unpacks all add fields"""
        if enable:
            add_user_label.pack(pady=5)
            Accounts_box.pack(pady=5)
            add_acc_label.pack(pady=5)
            add_acc_entry.pack(pady=5)
            add_pwd_label.pack(pady=5)
            add_pwd_entry.pack(pady=5)
            selected_account()  # Call the selected_account function to handle the editing of Accounts_box
            add_button.pack(pady=10)
        else:
            add_acc_label.pack_forget()
            add_acc_entry.pack_forget()
            add_pwd_label.pack_forget()
            add_pwd_entry.pack_forget()
            add_user_label.pack_forget()  # Hide the label for adding a new account
            Accounts_box.pack_forget()
            add_button.pack_forget()
            add_acc_entry.delete(0, tk.END)
            add_pwd_entry.delete(0, tk.END)
            Accounts_box.set(Accounts[0])

    # Used to unpack all master fields
    def toggle_master(enable):
        """Pacs and Unpacks all master"""
        if enable:
            master_label.pack(pady=5)
            master_entry.pack(pady=5)
            master_button.pack(pady=10)
        else:
            master_entry.pack_forget()
            master_label.pack_forget()
            master_button.pack_forget()
            reset()

    # Used to unpack all search fields
    def toggle_search(enable):
        """Packs and unpacks all search fields"""
        if enable:
            search_label.pack(pady=5)
            search_entry.pack(pady=5)
            search_button.pack(pady=10)
            search_listbox.delete("1.0", tk.END)  # Clear the text in the scrolled text widget
        else:
            search_label.pack_forget()
            search_entry.pack_forget()
            search_button.pack_forget()
            search_entry.delete(0, tk.END)
            # Use the after method to display the search_listbox after 10 seconds
            search_listbox.after(60000, lambda: search_listbox.pack_forget())

    # Used to unpack all edit fields
    def toggle_edit(enable):
        """Packs and unpacks all edit fields"""
        if enable:
            edit_label.pack(pady=5)
            edit_search.pack(pady=5)
            edit_label_user.pack(pady=5)
            edit_entry_username.pack(pady=5)
            edit_label_acc.pack(pady=5)
            edit_entry_account.pack(pady=5)
            edit_label_pass.pack(pady=5)
            edit_entry_password.pack(pady=5)
            edit_button.pack(pady=10)
        else:
            edit_label.pack_forget()
            edit_label_acc.pack_forget()
            edit_search.pack_forget()
            edit_label_user.pack_forget()
            edit_label_pass.pack_forget()
            edit_entry_account.pack_forget()
            edit_entry_username.pack_forget()
            edit_entry_password.pack_forget()
            edit_button.pack_forget()
            edit_entry_account.delete(0, tk.END)
            edit_entry_username.delete(0, tk.END)
            edit_entry_password.delete(0, tk.END)

    # Used to unpack all delete fields
    def toggle_delete(enable):
        """Packs and unpacks all delete fields"""
        if enable:
            delete_entry_label.pack(pady=5)
            delete_entry.pack(pady=5)
            delete_Button.pack(pady=10)
        else:
            delete_entry_label.pack_forget()
            delete_entry.pack_forget()
            delete_Button.pack_forget()
            delete_entry.delete(0, tk.END)

    # Used to pack and unpack all upload fields
    def toggle_upload(enable):
        """Packs and unpacks all upload fields"""
        if enable:
            upload_label.pack(pady=5)
            upload_button.pack(pady=10)
        else:
            upload_label.pack_forget()
            upload_button.pack_forget()

    # Used to get the value from the main combobox
    def get_value(event=None):
        """Return the value from the combobox"""
        selected_value = items.get()
        if selected_value == "Options":
            main_label.config(text="Please select an action!", fg="red")
            main_label.pack()  # Show the main label when "Options" is selected
        elif selected_value == "add":
            toggle_add_fields(True)
            toggle_edit(False)
            toggle_delete(False)
            toggle_search(False)
            toggle_master(False)
            search_listbox.pack_forget()
        elif selected_value == "view":
            toggle_master(True)
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
            toggle_add_fields(False)
            search_listbox.pack_forget()
        elif selected_value == "search":
            toggle_master(True)
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
            toggle_add_fields(False)
        elif selected_value == "delete":
            toggle_delete(True)
            toggle_search(False)
            toggle_edit(False)
            toggle_add_fields(False)
            toggle_master(False)
            search_listbox.pack_forget()
        elif selected_value == "edit":
            toggle_edit(True)
            toggle_search(False)
            toggle_delete(False)
            toggle_master(False)
            toggle_add_fields(False)
            search_listbox.pack_forget()
        elif selected_value == "upload":
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
            toggle_master(True)
            toggle_add_fields(False)
            search_listbox.pack_forget()
        else:
            return "Select a value from the dropdown list"

    # Main Combobox
    Task_box.bind('<<ComboboxSelected>>', get_value)
    Task_label.pack(pady=5)
    Task_box.pack(pady=5)

    # Define a dictionary that maps each entry field to its corresponding next field or button
    entry_mapping = {
        add_acc_entry: add_pwd_entry,
        add_pwd_entry: add_button,
        master_entry: master_button,
        search_entry: search_button,
        edit_search: edit_entry_account,
        edit_entry_account: edit_entry_username,
        edit_entry_username: edit_entry_password,
        edit_entry_password: edit_button,
        delete_entry: delete_Button,
        upload_button: upload_button,
    }

    # Define a function to handle Enter key press
    def handle_enter(event):
        focused_widget = window.focus_get()
        if focused_widget in entry_mapping:
            next_widget = entry_mapping[focused_widget]
            next_widget.focus()
        elif focused_widget in [add_button, master_button, search_button, edit_button, delete_Button, upload_button]:
            focused_widget.invoke()  # Simulate a button click

    # Bind the <Return> key event to all relevant entry fields and buttons
    for widget in entry_mapping.keys():
        widget.bind("<Return>", handle_enter)
    for button in [add_button, master_button, search_button, edit_button, delete_Button, upload_button]:
        button.bind("<Return>", handle_enter)

    window.mainloop()


if __name__ == '__main__':
    # Configure logging to write to a file and print to the console
    logging.basicConfig(filename="password_manager.log", level=logging.INFO,
                        format='%(message)s - %(asctime)s - %(levelname)s ', datefmt='%Y-%m-%d %H:%M:%S')

    gui()
