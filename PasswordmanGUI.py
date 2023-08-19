import tkinter as tk
import tkinter.ttk
import sqlite3
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


# main funcs
def add(username, account, password, message_label, toggle_add_fields, window):
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

        toggle_add_fields(False)

        message_label.config(text="Account added successfully!", fg="green")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())


def view():
    return NotImplementedError


def edit(search, account, username, password, message_label, edit_search, toggle_edit, window):
    if search.strip() == "" or account.strip() == "" or username.strip() == "" or password.strip() == "":
        message_label.config(text="Fields Cannot Be Empty", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())
        return
    connection = sqlite3.connect("Passwords.db")
    cursor = connection.cursor()

    result = cursor.execute("SELECT USERNAME, ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (search,))

    existing_data = result.fetchone()
    if not existing_data:
        message_label.config(text="Account not found", fg="red")
        message_label.pack()
        edit_search.delete(0, tk.END)
        window.after(2000, lambda: message_label.pack_forget())
    else:
        new_account = account.strip() if account.strip() else existing_data[1]
        new_username = username.strip() if username.strip() else existing_data[0]
        new_password = password.strip() if password.strip() else existing_data[2]

        cursor.execute("UPDATE manager SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE USERNAME=?",
                       (new_account.title(), new_username.title(), new_password, search))
        connection.commit()
        message_label.config(text="Account updated", fg="green")
        message_label.pack()
        toggle_edit(False)
        window.after(2000, lambda: message_label.pack_forget())

    connection.close()


def delete(Account, message_label, toggle_delete, window):
    if Account.strip() == "":
        message_label.config(text="Please Enter An Account", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())  # Hide the message after 2000ms
        return  # Return to prevent further execution of the function

    connection = sqlite3.connect('Passwords.db')
    cursor = connection.cursor()
    results = cursor.execute("SELECT USERNAME,ACCOUNT, PASSWORD FROM manager WHERE USERNAME=?", (Account.title(),))
    results = results.fetchall()

    if not results:
        message_label.config(text="Account does not exist!", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())  # Hide the message after 2000ms
    else:
        cursor.execute("DELETE FROM manager WHERE USERNAME=?", (Account.strip().title(),))
        connection.commit()
        toggle_delete(False)
        message_label.config(text="Account deleted", fg="green")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())  # Hide the message after 2000ms

    connection.close()


def upload(Passcode, message_label, upload_entry, toggle_upload, window):
    with open("Passcodeupload.txt", "r") as file:
        code = file.readline().strip()
    if Passcode.strip() == "":
        message_label.config(text="Passcode Field Cannot Be Empty!", fg="red")
        message_label.pack()
        window.after(2000, lambda: message_label.pack_forget())
    if Passcode.strip() == code:
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

                print(f"Updated file ID: {update_file.get('id')} & name {file_metadata.get('name')}")
                message_label.config(text="File Updated Successfully", fg="green")
                message_label.pack()
                window.after(2000, lambda: message_label.pack_forget())
            else:
                media = MediaFileUpload(file_path)
                upload_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"Uploaded file ID: {upload_file.get('id')} & name {file_metadata.get('name')}")
                message_label.config(text="File Uploaded To Google Drive", fg="green")
                message_label.pack()
                window.after(2000, lambda: message_label.pack_forget())
        except HttpError as error:
            print(f'An error occurred: {error}')
            message_label.config(text="An error occurred during upload", fg="red")
            message_label.pack()
            window.after(2000, lambda: message_label.pack_forget())
    else:
        message_label.config(text="Invalid Passcode!", fg="red")
        message_label.pack()
        upload_entry.delete(0, tk.END)
        window.after(2000, lambda: message_label.pack_forget())


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

    # Main Label
    main_label = tk.Label(text="Welcome To The Password Manager", font=("Lato", 20))
    main_label.pack()

    # Main taskbox for adding
    Tasks = ["Options", "add", "view", "edit", "delete", "upload", "search"]
    Task_label = tk.Label(window, text="Select your task:", font=("Lato", 15))
    items = tk.StringVar()
    Task_box = tk.ttk.Combobox(window, textvariable=items, font=("oswald", 20))
    Task_box["values"] = Tasks
    Task_box["state"] = 'readonly'

    # Accounts adding ComboBox
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

    # Add Function Fields
    add_user_label = tk.Label(window, text="Add service account to add: ")
    add_acc_label = tk.Label(window, text="Enter your account: ")
    add_pwd_label = tk.Label(window, text="Enter your password: ")
    add_acc_entry = tk.Entry(window, font=("oswald", 20))
    add_pwd_entry = tk.Entry(window, font=("oswald", 20), show="*")
    add_message_label = tk.Label(window, text="", font=("oswald", 14))
    add_button = tk.Button(window, text="Add Account",
                           command=lambda: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                               add_message_label, toggle_add_fields, window),
                           font=("oswald", 20))

    # Master Function Fields
    master_label = tk.Label(window, text="Enter Master Password: ")
    master_entry = tk.Entry(window, font=("oswald", 20), show="*")
    master_main_label = tk.Label(window, text="", font=("oswald", 14))
    master_button = tk.Button(window, text="Check",
                              command=lambda: master(master_entry.get(), master_main_label, master_entry, toggle_master,
                                                     items,
                                                     toggle_search, window), font=("oswald", 20))
    # Search Function Fields
    search_label = tk.Label(window, text="Enter Account To Search: ")
    search_entry = tk.Entry(window, font=("oswald", 20))
    search_main_label = tk.Label(window, text="", font=("oswald", 14))
    search_button = tk.Button(window, text="Search",
                              command=lambda: exist(search_entry.get(), search_main_label, toggle_search, window),
                              font=("oswald", 20))
    # Edit Function Fields
    edit_label = tk.Label(window, text="Enter Account To Edit: ")
    edit_search = tk.Entry(window, font=("oswald", 20))
    edit_label_user = tk.Label(window, text="Enter Updated Account: ")
    edit_entry_username = tk.Entry(window, font=("oswald", 20))
    edit_label_acc = tk.Label(window, text="Enter Updated Username: ")
    edit_entry_account = tk.Entry(window, font=("oswald", 20))
    edit_label_pass = tk.Label(window, text="Enter Updated Password: ")
    edit_entry_password = tk.Entry(window, font=("oswald", 20), show="*")
    edit_main_label = tk.Label(window, text="", font=("oswald", 14))
    edit_button = tk.Button(window, text="Edit",
                            command=lambda: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                                 edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                                 window), font=("oswald", 20))

    # Delete Function Fields
    delete_main_label = tk.Label(window, text="", font=("oswald", 14))
    delete_entry_label = tk.Label(window, text="Enter Account to Be Deleted: ", )
    delete_entry = tk.Entry(window, font=("oswald", 20))
    delete_Button = tk.Button(window, text="Delete", command=lambda: delete(delete_entry.get(), delete_main_label,
                                                                            toggle_delete, window))

    upload_label = tk.Label(window, text="Enter Upload Passcode: ", )
    upload_entry = tk.Entry(window, font=("oswald", 20), show="*")
    upload_main_label = tk.Label(window, text="", font=("oswald", 14))
    upload_button = tk.Button(window, text="Upload", command=lambda: upload(upload_entry.get(), upload_main_label,
                                                                            upload_entry, toggle_upload, window))

    def reset():
        Task_box.set(Tasks[0])

    # Used to unpack all add fields
    def toggle_add_fields(enable):
        """Packs and Unpacks all add fields"""
        if enable:
            add_user_label.pack()
            Accounts_box.pack()
            add_acc_label.pack()
            add_acc_entry.pack()
            add_pwd_label.pack()
            add_pwd_entry.pack()
            selected_account()  # Call the selected_account function to handle the editing of Accounts_box
            add_button.pack()
        else:
            add_acc_label.pack_forget()
            add_acc_entry.pack_forget()
            add_pwd_label.pack_forget()
            add_pwd_entry.pack_forget()
            add_user_label.pack_forget()  # Hide the label for adding a new account
            Accounts_box.pack_forget()
            add_button.pack_forget()

    # Used to unpack all master fields
    def toggle_master():
        """Unpacks all master"""
        master_entry.pack_forget()
        master_label.pack_forget()
        master_button.pack_forget()

    # Used to unpack all search fields
    def toggle_search(enable):
        """Packs and unpacks all search fields"""
        if enable:
            search_label.pack()
            search_entry.pack()
            search_button.pack()
        else:
            search_label.pack_forget()
            search_entry.pack_forget()
            search_button.pack_forget()

    # Used to unpack all edit fields
    def toggle_edit(enable):
        """Packs and unpacks all edit fields"""
        if enable:
            edit_label.pack()
            edit_search.pack()
            edit_label_user.pack()
            edit_entry_username.pack()
            edit_label_acc.pack()
            edit_entry_account.pack()
            edit_label_pass.pack()
            edit_entry_password.pack()
            edit_button.pack()
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

    # Used to unpack all delete fields
    def toggle_delete(enable):
        """Packs and unpacks all delete fields"""
        if enable:
            delete_entry_label.pack()
            delete_entry.pack()
            delete_Button.pack()
        else:
            delete_entry_label.pack_forget()
            delete_entry.pack_forget()
            delete_Button.pack_forget()

    # Used to pack and unpack all upload fields
    def toggle_upload(enable):
        """Packs and unpacks all upload fields"""
        if enable:
            upload_label.pack()
            upload_entry.pack()
            upload_button.pack()
        else:
            upload_label.pack_forget()
            upload_entry.pack_forget()
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
            toggle_master()
        elif selected_value == "view":
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
            toggle_add_fields(False)
            view()
        elif selected_value == "search":
            master_label.pack()
            master_entry.pack()
            master_button.pack()
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
        elif selected_value == "delete":
            toggle_delete(True)
            toggle_search(False)
            toggle_edit(False)
            toggle_add_fields(False)
            toggle_master()
        elif selected_value == "edit":
            toggle_edit(True)
            toggle_search(False)
            toggle_delete(False)
            toggle_master()
            toggle_add_fields(False)
        elif selected_value == "upload":
            toggle_upload(True)
            toggle_search(False)
            toggle_delete(False)
            toggle_edit(False)
            toggle_master()
            toggle_add_fields(False)

        else:
            return "Select a value from the dropdown list"

    # Main Combobox
    Task_box.bind('<<ComboboxSelected>>', get_value)
    Task_label.pack()
    Task_box.pack()

    # Add Bindings
    add_acc_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, toggle_add_fields, window))
    add_pwd_entry.bind("<Return>", lambda event: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                                     add_message_label, toggle_add_fields, window))
    add_button.config(command=lambda: add(selected_account, add_acc_entry.get(), add_pwd_entry.get(),
                                          add_message_label, toggle_add_fields, window))
    # Master Bindings
    master_entry.bind("<Return>", lambda event: master(master_entry.get(), master_main_label, master_entry,
                                                       items.get(), toggle_master, toggle_search, window))
    master_button.config(command=lambda: master(master_entry.get(), master_main_label, master_entry,
                                                items.get(), toggle_master, toggle_search, window))
    # Search binding
    search_entry.bind("<Return>", lambda event: exist(search_entry.get(), search_main_label, toggle_search, window))
    search_button.config(command=lambda: exist(search_entry.get(), search_main_label, toggle_search, window))

    # Edit binding
    edit_search.bind("<Return>",
                     lambda event: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                        edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                        window))
    edit_entry_account.bind("<Return>",
                            lambda event: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                               edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                               window))
    edit_entry_username.bind("<Return>",
                             lambda event: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                                edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                                window))
    edit_entry_password.bind("<Return>",
                             lambda event: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                                edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                                window))

    edit_button.config(command=lambda: edit(edit_search.get(), edit_entry_account.get(), edit_entry_username.get(),
                                            edit_entry_password.get(), edit_main_label, edit_search, toggle_edit,
                                            window))
    # Delete Bindings
    delete_entry.bind("<Return>", lambda event: delete(delete_entry.get(), delete_main_label, toggle_delete, window))
    delete_Button.config(command=lambda: delete(delete_entry.get(), delete_main_label, toggle_delete, window))

    # Upload Bindings
    upload_entry.bind("<Return>",
                      lambda event: upload(upload_entry.get(), upload_main_label, upload_entry, toggle_upload, window))
    upload_button.config(
        command=lambda: upload(upload_entry.get(), upload_main_label, upload_entry, toggle_upload, window))
    window.mainloop()


if __name__ == '__main__':
    gui()
