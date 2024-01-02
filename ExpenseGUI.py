import datetime
import logging
import os
import pprint
from numerize import numerize
import sqlite3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable
import pandas as pd
from dateutil.relativedelta import relativedelta
from tkcalendar import Calendar
from ttkthemes import ThemedStyle
import openpyxl
import matplotlib.pyplot as plt
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore


def create_database():
    try:
        connection = sqlite3.connect('Expenses.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Date DATE NOT NULL,
                Category TEXT NOT NULL,
                Description TEXT,
                Amount FLOAT NOT NULL,
                Available FLOAT  NOT NULL,
                Total FLOAT NOT NULL)
        ''')
        connection.commit()
        logging.info('Created database!')
        connection.close()
    except sqlite3.DatabaseError as error:
        logging.info(f'Error creating database! {error}')


def show_message(message_label: tk.Label, text: str, colour: str, duration=2000) -> None:
    """
       Display a message on the GUI.

       Args:
           message_label (tk.Label): The label widget to display the message.
           text (str): The message text.
           colour (str): The color of the message text.
           duration (int, optional): Duration in milliseconds to display the message. Default is 2000ms.
       """
    message_label.config(text=text, fg=colour)
    message_label.pack(pady=10)
    message_label.after(duration, lambda: message_label.pack_forget())


def upload(folder_name: str, filename: str):
    """
        Upload the database file to Google Drive.

        This function uploads the database file to a designated folder in Google Drive
        after validating a provided passcode.

        Args:
            folder_name: The name of the folder to upload to Google Drive.
            filename: The name of the database file to upload to folder

    """
    global creds
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json'):
            creds = Credentials.from_authorized_user_file(
                r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Drive_Credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', 'w') as token:
                token.write(creds.to_json())
    except Exception as error:
        logging.info(f"An error occurred {error}!")

    try:
        service = build('drive', 'v3', credentials=creds)

        response = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive').execute()

        if not response['files']:
            file_metadata = {
                "name": f"{folder_name}",
                "mimeType": "application/vnd.google-apps.folder",
            }

            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        file_metadata = {
            "name": f"{filename}",
            "parents": [folder_id]
        }

        file_path = fr"C:\Users\huzai\PycharmProjects\Python-projects-1\{filename}"
        # Search for the existing file in Google Drive
        existing_file = service.files().list(
            q=f"name='{filename}' and parents='{folder_id}'",
            spaces='drive').execute()

        if existing_file['files']:
            existing_file_id = existing_file['files'][0]['id']

            media = MediaFileUpload(file_path, resumable=True)
            update_file = service.files().update(fileId=existing_file_id, media_body=media).execute()
            logging.info(f"Updated file: {filename} --> {folder_name}")
        else:
            media = MediaFileUpload(file_path)
            upload_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logging.info(f"Uploaded file to drive {filename} --> {folder_name} {upload_file.get('id')}")
    except HttpError as error:
        logging.info(f'An error occurred: {error}')


def deposit(date: Calendar, value: str, message_label: tk.Label, toggle_deposit: Callable) -> None:
    """
    Adds an initial deposit value for the selected month to the database.

    Args:
        date (Calendar): The selected date from a calendar widget.
        value (str): The deposit amount to add to the database.
        message_label (tk.Label): The label widget to display status messages.
        toggle_deposit (Callable): A callable function to toggle the deposit feature.

    Returns:
        None: This function does not return a value, but it adds the deposit to the database.

    """
    try:
        selected_date = date.parse_date(date.get_date())
        connection = sqlite3.connect('Expenses.db')
        cursor = connection.cursor()
        formatted_date = selected_date.strftime('%Y-%m')
        value = float(value)

        if value <= 0:
            show_message(message_label, text="Amount should be greater than 0!", colour="red")
            logging.info(f"Invalid Input!")
        else:
            cursor.execute("SELECT Available, Total FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category "
                           "= ?",
                           (formatted_date, "MONTHLY DEPOSIT!"))
            existing_values = cursor.fetchone()
            if existing_values:
                existing_available, initial_amount = existing_values
                new_available = existing_available + value
                new_total = initial_amount + value
                # Update the existing deposit record
                cursor.execute(
                    "UPDATE Transactions SET Date = ?, Amount = ?, Available = ?, Total = ? "
                    "WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                    (selected_date.strftime('%Y-%m-%d'), value, new_available, new_total, formatted_date,
                     "MONTHLY DEPOSIT!"))
                # Update Available and Total columns
                cursor.execute("UPDATE Transactions SET Available = ?, Total = ? WHERE strftime('%Y-%m', Date) = ?",
                               (new_available, new_total, formatted_date))
                show_message(message_label,
                             text=f"Deposit for month: {selected_date.strftime('%B')}\nValue: £{value} is Successful!\n"
                                  f"Current balance: £{new_available}\nTotal amount deposited: £{new_total}",
                             colour="green", duration=7000)
                messagebox.showinfo(f"{selected_date.strftime('%B')} TRANSCTIONS", f"Value: £{value} is Successful!\n"
                                                                                   f"Current balance: £{new_available}"
                                                                                   f"\nTotal amount deposited: £{new_total}")
            else:
                cursor.execute("INSERT INTO Transactions (Date, Category, Amount, Available, Total) VALUES (?, ?, ?, "
                               "?, ?)",
                               (selected_date.strftime('%Y-%m-%d'), "MONTHLY DEPOSIT!", value, value, value))
                show_message(message_label,
                             text=f"Deposit for month: {selected_date.strftime('%B')}\nValue: £{value} is Successful!\n",
                             colour="green", duration=7000)
                messagebox.showinfo(f"{selected_date.strftime('%B')} Deposit", f"Deposit of £{value} Successful")
            toggle_deposit(False)
            connection.commit()
            connection.close()
            logging.info("Successfully deposited the amount!")
    except sqlite3.Error as error:
        show_message(message_label, text=f"SQLite error: {error}", colour="red")
        logging.error(f"SQLite error: {error}")
    except (TypeError, ValueError) as error:
        show_message(message_label, text=f"An error occurred: {error}", colour="red")
        logging.error(f"An error occurred: {error}")


def deduct(date: Calendar, category: Callable, description: str, value: str, message_label: tk.Label,
           toggle_deduct: Callable) -> None:
    """
    Deducts an expense from the selected date's budget and updates the database.

    Args:
        date (Calendar): The selected date from a calendar widget.
        category (Callable): A function to select the expense category.
        description (str): A description of the expense.
        value (str): The amount of the expense to deduct.
        message_label (tk.Label): The label widget to display status messages.
        toggle_deduct (Callable): A callable function to toggle the deduct feature.

    Returns:
        None: This function does not return a value but deducts the expense and updates the database.

    """

    try:
        selected_date = date.parse_date(date.get_date())
        option = category()
        formatted_date = selected_date.strftime('%Y-%m')
        value = float(value)
        connection = sqlite3.connect("Expenses.db")
        cursor = connection.cursor()
        # Fetch the existing total deposit for the current month
        cursor.execute("SELECT Available, Total FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                       (formatted_date, "MONTHLY DEPOSIT!"))
        existing_values = cursor.fetchone()
        if value <= 0 or option.strip() == "":
            show_message(message_label, text="Invalid Entry!\n(check value > 0 & category is not empty)", colour="red")
            logging.info("Value should be greater than 0! or Category is empty")
        else:
            if existing_values is None:
                show_message(message_label, text=f"No deposit made for the month {selected_date.strftime('%B')}",
                             colour="red")
                logging.info("No funds allocated for the month!")
            else:
                existing_available, existing_total = existing_values
                if value > existing_available:
                    show_message(message_label, text="Insufficient Funds!", colour="red")
                    logging.info("Insufficient funds in the database add more!")
                else:
                    new_available = existing_available - value
                    if description.strip() == "":
                        description = "N/A"
                    # Entering main category to db
                    cursor.execute("INSERT INTO Transactions (Date, Category, Description, Amount, Available, Total) "
                                   "VALUES (?, ?, ?, ?, ?, ?)",
                                   (selected_date.strftime('%Y-%m-%d'), option, description, value,
                                    new_available, existing_total))
                    cursor.execute("UPDATE Transactions SET Available = ? WHERE strftime('%Y-%m', Date) = ?",
                                   (new_available, formatted_date))
                    show_message(message_label, text="Successfully added!", colour='green')
                    logging.info("Successfully Inserted & Updated the data into the database")
            toggle_deduct(False)
            connection.commit()
            connection.close()
    except sqlite3.Error as error:
        show_message(message_label, text=f"SQLite error: {error}", colour="red")
        logging.error(f"SQLite error: {error}")
    except (TypeError, ValueError) as error:
        show_message(message_label, text=f"An error occurred: {error}", colour="red")
        logging.error(f"An error occurred: {error}")


def convert(convert_type: str, calendar: Callable, message_label: tk.Label) -> None:
    """
    Converts and exports data based on the selected conversion type.

    Args:
        convert_type (str): The type of conversion to perform (e.g., 'Pandas', 'CSV', etc.).
        calendar (Callable): A function to select a specific calendar date or range.
        message_label (tk.Label): The label widget to display status messages.

    Returns:
        None: This function does not return a value but performs the specified data conversion and export.

    """
    if convert_type == "Excel":
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)

        df = pd.read_sql_query(query, connection, params=params)  # NOQA

        if df.bool:
            excel_file = f'{month}_sheet.xlsx'
            df['Total Spent'] = df['Amount'].iloc[1:].cumsum()
            columns_to_convert = ["Amount", "Available", "Total"]
            for column in columns_to_convert:
                df[column] = df[column].apply(lambda x: '£' + numerize.numerize(int(x)))
            # df.drop(columns=['Description'], inplace=True)
            df['Total Spent'].fillna(0, inplace=True)
            df['Total Spent'] = df['Total Spent'].apply(lambda x: '£' + numerize.numerize(int(x)))
            df.to_excel(excel_file, index=False, engine='openpyxl')
            folder_name = f"{month}-{year}"
            upload(folder_name, excel_file)

            show_message(message_label, text=f"{excel_file}\nCreated Successfully!", colour="green")
            logging.info(f"xlsx file successful!")
        else:
            show_message(message_label, text=f"Check {month} data!", colour="red")
            logging.info(f"{month} doesnt have values to create dataframe")

    elif convert_type == 'CSV' or convert_type == 'Pandas':
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)

        df = pd.read_sql_query(query, connection, params=params)  # NOQA

        if df.bool:
            df['Total Spent'] = df['Amount'].iloc[1:].cumsum()
            columns_to_convert = ["Amount", "Available", "Total"]
            for column in columns_to_convert:
                df[column] = df[column].apply(lambda x: '£' + numerize.numerize(int(x)))
            df['Total Spent'].fillna(0, inplace=True)
            df['Total Spent'] = df['Total Spent'].apply(lambda x: '£' + numerize.numerize(int(x)))

            csv_file = f"{month}_pandas_file.csv"
            folder_name = f"{month}-{year}"
            df.to_csv(csv_file, index=False)
            upload(folder_name, csv_file)

            show_message(message_label, text=f"{csv_file}\nCreated Successfully!", colour="green")
            logging.info(f"CSV file successful!")
        else:
            show_message(message_label, text=f"Check {month} {year} data!", colour="red")
            logging.info(f"{month} {year} doesnt have values to create dataframe")
    elif convert_type == "Pie Chart":
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)

        df = pd.read_sql_query(query, connection, params=params)  # NOQA
        if df.bool:

            df = df[df['Category'] != 'MONTHLY DEPOSIT!']

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

            category_amount_df = df.groupby('Category')['Amount'].sum()
            ax1.pie(category_amount_df, labels=category_amount_df.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title(f'Spending by Category for {month} {year}')

            ax2.pie(df[['Total', 'Available']].iloc[0], labels=['Total', 'Available'], autopct='%1.1f%%', startangle=90)
            ax2.set_title(f'Total and Available Amount for {month} {year}')

            plt.tight_layout()
            fig_name = f"{month}_Pie_Chart.png"
            folder_name = f"{month}-{year}"
            fig.savefig(fig_name)
            upload(folder_name, fig_name)

            show_message(message_label, text="Pie Chart Successfully Created!", colour='green')
            logging.info(f"Pie chart successful created!")
        else:
            show_message(message_label, text=f"Check {month} {year} data!", colour="red")
            logging.info(f"{month} {year} doesnt have values to create dataframe")

    elif convert_type == 'Bar Graph':
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)

        df = pd.read_sql_query(query, connection, params=params)  # NOQA
        df['Date'] = pd.to_datetime(df['Date'])

        if df.bool:
            df = df[df['Category'] != 'MONTHLY DEPOSIT!']

            category_amount_df = df.groupby('Category')['Amount'].sum()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            category_amount_df.plot(kind='bar', ax=ax1)

            df['Cumulative_Amount'] = df['Amount'].cumsum()
            df['Available_overtime'] = df['Total'] - df['Cumulative_Amount']
            df['Day'] = df['Date'].dt.day
            total_available = df[['Day', 'Available_overtime']].set_index('Day')
            total_available.plot(kind='barh', ax=ax2)

            ax1.set_xlabel('Category')
            ax1.set_ylabel('Amount / £')
            ax1.set_title(f'Category-wise Spending for {month} {year}')
            ax2.set_xlabel('Amount / £')
            ax2.set_ylabel('Day')
            ax2.set_title(f'Available for {month} {year} per date')

            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=360, ha='center')
            ax2.set_xticklabels(ax2.get_xticklabels(), rotation=360, ha='center')

            plt.tight_layout()
            fig_name = f"{month}_Bar_Graph.png"
            folder_name = f"{month}-{year}"
            fig.savefig(fig_name)
            upload(folder_name, fig_name)

            show_message(message_label, text="Bar Graph Successfully Created!", colour='green')
            logging.info(f"Bar graph successful created!")
        else:
            show_message(message_label, text=f"Check {month} {year} data!", colour="red")
            logging.info(f"{month} {year} doesnt have values to create dataframe")

    elif convert_type == 'Line Chart':
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)

        df = pd.read_sql_query(query, connection, params=params)  # NOQA
        df['Date'] = pd.to_datetime(df['Date'])

        if df.bool:
            df = df[df['Category'] != "MONTHLY DEPOSIT!"]
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            categorized = df.groupby("Category")["Amount"].sum()
            ax1.plot(categorized.index, categorized.values)
            ax1.set_xlabel('Categories')
            ax1.set_ylabel('Total Amount')
            ax1.set_title('Expenses by Category')
            ax1.tick_params(axis='x', rotation=360)

            df['Cumulative_Amount'] = df['Amount'].cumsum()
            df['Available_overtime'] = df['Total'] - df['Cumulative_Amount']
            df["Day"] = df['Date'].dt.day.round().astype(int)
            ax2.plot(df['Day'], df['Available_overtime'])
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Amount / £')
            ax2.set_title(f'Available for {month} {year} per date')
            ax2.tick_params(axis='x', rotation=360)

            fig_name = f"{month}_Line_Chart.png"
            folder_name = f"{month}-{year}"
            plt.savefig(fig_name)
            upload(folder_name, fig_name)

            show_message(message_label, text="Line Chart Successfully Created!", colour='green')
            logging.info(f"Line Chart successful created!")

        else:
            show_message(message_label, text=f"Check {month} {year} data!", colour="red")
            logging.info(f"{month} {year} doesnt have values to create dataframe")

    elif convert_type == 'Histogram':
        month, year = calendar()
        connection = sqlite3.connect('Expenses.db')
        selected = datetime.datetime.strptime(month, '%B')
        formatted = selected.replace(year=int(year)).strftime('%Y-%m')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? ORDER BY Date"
        params = (formatted,)
        df = pd.read_sql_query(query, connection, params=params)  # NOQA
        df['Date'] = pd.to_datetime(df['Date'])

        if not df.empty:
            df = df[df['Category'] != 'MONTHLY DEPOSIT!']

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            amounts = df['Amount'].tolist()

            ax1.hist(amounts, bins=10)
            ax1.set_xlabel('Amount')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Expense Amount Histogram')

            categorized = df.groupby("Category")["Amount"].sum()
            ax2.bar(categorized.index, categorized.values)
            ax2.set_xlabel('Categories')
            ax2.set_ylabel('Total Amount')
            ax2.set_title('Expenses by Category')
            ax2.tick_params(axis='x', rotation=360)

            plt.tight_layout()
            fig_name = f"{month}_Histogram.png"
            folder_name = f"{month}-{year}"
            fig.savefig(fig_name)
            upload(folder_name, fig_name)

            show_message(message_label, text="Histogram Successfully Created!", colour='green')
            logging.info(f"Histogram successfully created!")
        else:
            show_message(message_label, text=f"Check {month} data!", colour="red")
            logging.info(f"{month} doesn't have values to create a dataframe")


def view(date: Calendar, message_label: tk.Label, view_box: tk.scrolledtext.ScrolledText) -> None:
    """
    Displays and retrieves expense data for the selected month.

    Args:
        date (Calendar): The selected date from a calendar widget.
        message_label (tk.Label): The label widget to display status messages.
        view_box (tk.scrolledtext.ScrolledText): The text widget for displaying expense data.

    Returns:
        None: This function does not return a value but displays the expense data in the view_box.

    """
    try:
        selected_date = date.parse_date(date.get_date())
        connection = sqlite3.connect("Expenses.db")
        cursor = connection.cursor()

        start_date = selected_date.strftime('%Y-%m-%d')
        end_date = (selected_date + relativedelta(day=31)).strftime('%Y-%m-%d')

        # or use
        # next_month = selected_date.replace(day=28) + datetime.timedelta(days=4)
        # end_date = next_month - datetime.timedelta(days=next_month.day)
        view_box.config(state='normal')
        view_box.delete("1.0", tk.END)

        results = cursor.execute(
            "SELECT Date, Category, Amount, Available, Total FROM Transactions WHERE Date BETWEEN ? AND ?"
            "ORDER BY Date",
            (start_date, end_date))

        data = results.fetchall()

        if not data:
            view_box.grid_remove()
            show_message(message_label, text=f"No results found for the month of {selected_date.strftime('%B %Y')}",
                         colour="red")
            logging.info(f"No matches found for the month of {selected_date.strftime('%B %Y')}")
        else:
            show_message(message_label, text="Getting results......", colour="green")
            logging.info(f"Match found! for the month of {selected_date.strftime('%B %Y')}")

            view_box.insert(tk.END, f"Expenses for the Month of {selected_date.strftime('%B %Y')}\n\n", "custom_font")
            view_box.insert(tk.END, "S.NO\tDATE\t\tCATEGORY\t\t\t\tSPENT\n", "custom_font")

            spent = 0
            available = 0
            total_deposit = 0

            for index, row in enumerate(data, start=1):
                date_str = row[0]
                category = row[1]
                amount = row[2]

                view_box.insert(tk.END, f"{index}\t{date_str}\t\t{category}\t\t\t\t£ {amount}\n", "custom_font")
                if category != "MONTHLY DEPOSIT!":
                    spent += amount
                    available = row[3]
                    total_deposit = row[4]
                else:
                    available = row[3]
                    total_deposit = row[4]
            view_box.insert(tk.END, f"\nTOTAL AVAILABLE: £{numerize.numerize(available)}\n"
                                    f"TOTAL SPENT: £{numerize.numerize(spent)}\n"
                                    f"TOTAL DEPOSITED: £{numerize.numerize(total_deposit)}", "custom_font")
            view_box.config(state='disabled')
            view_box.after(2500, lambda: view_box.grid(row=3, column=0))

        connection.close()
    except sqlite3.Error as error:
        show_message(message_label, text=f"SQLite error: {error}", colour="red")
        logging.error(f"SQLite error: {error}")
    except (TypeError, ValueError) as error:
        show_message(message_label, text=f"An error occurred: {error}", colour="red")
        logging.error(f"An error occurred: {error}")


def delete(date: Calendar, category: Callable, message_label: tk.Label, toggle_delete: Callable) -> None:
    """
    Delete data from the database for the selected date.

    Parameters:
        date (Calendar): The Tkinter Calendar widget used to select a date.
        category (Callable): Calls the category getting function.
        message_label (tk.Label): The Tkinter Label widget for displaying messages.
        toggle_delete (Callable): A function for toggling the delete mode in the GUI.

    Returns:
        None
    """
    try:
        option = category()
        selected_date = date.parse_date(date.get_date())
        connection = sqlite3.connect("Expenses.db")
        cursor = connection.cursor()
        print(option)
        if option == "MONTHLY DEPOSIT!":
            results = cursor.execute("SELECT * FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                                     (selected_date.strftime('%Y-%m'), "MONTHLY DEPOSIT!"))
            if not results.fetchall():
                show_message(message_label, text=f"{selected_date} data not found!", colour='red')
                logging.info(f"{selected_date} deletion unsuccessful!")
            else:
                cursor.execute("DELETE FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                               (selected_date.strftime('%Y-%m'), "MONTHLY DEPOSIT!"))
                show_message(message_label, text=f"Deleted data for date {selected_date} & updated!", colour="green")
                logging.info(f"{selected_date} date data successfully deleted & updated!")
                connection.commit()
        else:
            results = cursor.execute("SELECT * FROM Transactions WHERE strftime('%Y-%m-%d', Date) = ? AND Category = ?",
                                 (selected_date.strftime('%Y-%m-%d'), option.capitalize()))
            if not results.fetchall():
                show_message(message_label, text=f"{selected_date} data not found!", colour='red')
                logging.info(f"{selected_date} deletion unsuccessful!")
            else:
                get_values = cursor.execute("SELECT Available, Amount, Total FROM Transactions WHERE"
                                            " strftime('%Y-%m-%d', Date)= ? AND Category = ?",
                                            (selected_date.strftime('%Y-%m-%d'), option.capitalize()))
                available, amount, total = 0, 0, 0
                for row in get_values.fetchall():
                    available += row[0]
                    amount += row[1]
                    total += row[2]
                updated_total = total + amount
                updated_available = available + amount
                cursor.execute("DELETE FROM Transactions WHERE strftime('%Y-%m-%d', Date)= ? AND Category = ?",
                               (selected_date, option.capitalize()))
                cursor.execute("UPDATE Transactions SET Available = ?, Total = ? WHERE strftime('%Y-%m', Date) = ?",
                               (updated_available, updated_total, selected_date.strftime('%Y-%m')))
                show_message(message_label, text=f"Deleted data for date {selected_date} & updated!", colour="green")
                logging.info(f"{selected_date} date data successfully deleted & updated!")
                connection.commit()
                toggle_delete(False)
        connection.close()
    except sqlite3.Error as error:
        show_message(message_label, text=f"SQLite error: {error}", colour="red")
        logging.error(f"SQLite error: {error}")
    except (TypeError, ValueError) as error:
        show_message(message_label, text=f"An error occurred: {error}", colour="red")
        logging.error(f"An error occurred: {error}")


def summary(selection: str, date: Callable, message_label: tk.Label, toggle_summary: Callable):
    """
        Generate and display summary charts based on the user's selection (Monthly or Yearly).

        Parameters:
            selection (str): The user's selection, either 'Monthly' or 'Yearly'.
            date (Callable): A function that returns the selected month and year.
            message_label (tk.Label): The Tkinter Label widget for displaying messages.
            toggle_summary (Callable): A function for toggling the summary display in the GUI.

        Returns:
            None
        """
    if selection == 'Monthly':
        month, year = date()
        formatted = datetime.datetime.strptime(month, "%B").replace(year=int(year)).strftime('%Y-%m')
        connection = sqlite3.connect('Expenses.db')
        query = "SELECT * FROM Transactions WHERE strftime('%Y-%m', Date)=?"
        params = (formatted,)
        df = pd.read_sql_query(query, connection, params=params)  # NOQA
        df['Date'] = pd.to_datetime(df['Date'])
        if df.bool:
            filtered = df[df['Category'] != 'MONTHLY DEPOSIT!'].copy()

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 10))

            # Categorized spending's for the moth
            categorized = filtered.groupby('Category')['Amount'].sum()
            categorized.plot(kind='bar', ax=ax1)

            ax1.set_xlabel('Category')
            ax1.set_ylabel('Amount / £')
            ax1.set_title(f'Category-wise Spending for {month} {year}')
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=360, ha='center')

            # Available over the month
            filtered['Day'] = filtered['Date'].dt.day
            filtered['Cumulative_Amount'] = filtered['Amount'].cumsum()
            filtered['Available_overtime'] = filtered['Total'] - filtered['Cumulative_Amount']
            available = filtered.groupby('Day')['Available_overtime'].last()
            available.plot(kind='line', ax=ax2)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Amount / £')
            ax2.set_title(f'Available for {month} {year} per date')
            ax2.tick_params(axis='x', rotation=360)

            # Total vs available over the month
            ax3.pie(filtered[['Total', 'Available']].iloc[0], labels=['Utilized', 'Available'], autopct='%1.1f%%',
                    startangle=90)
            ax3.set_title(f'Total and Available Amount for {month} {year}')

            # Spending's over the month
            daily_spending = filtered.groupby(filtered['Date'].dt.day)['Amount'].sum()
            daily_spending.plot(kind='line', ax=ax4, linewidth=1)
            ax4.set_xlabel('Date')
            ax4.set_ylabel('Amount / £')
            ax4.set_title(f"Spending's for {month} {year} per day")
            ax4.tick_params(axis='x', rotation=360)

            plt.tight_layout()
            fig_name = f"{month} {year} summary.png"
            fig.savefig(fig_name)
            folder_name = f"{month}-{year}"

            upload(folder_name, fig_name)
            show_message(message_label, text=f"Monthly Summary for {month}\nSuccessfully Generated!", colour='green')
            logging.info(f"{month} {year} Monthly summary generated successfully!")
        else:
            show_message(message_label, text=f"Check {month} {year} data!", colour="red")
            logging.info(f"{month} {year} doesnt have values to create dataframe")

    elif selection == 'Yearly':
        month, year = date()
        connection = sqlite3.connect('Expenses.db')
        query = "SELECT * FROM Transactions WHERE strftime('%Y', Date)=? ORDER BY Date"
        params = (year,)
        df = pd.read_sql_query(query, connection, params=params)  # NOQA

        df['Date'] = pd.to_datetime(df['Date'])

        if df.bool:
            filtered_df = df[df['Category'] != 'MONTHLY DEPOSIT!']
            category_amount_df = filtered_df.groupby('Category')['Amount'].sum()

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 10))

            # Categorized spending's for the  year
            category_amount_df.plot(kind='bar', ax=ax1)
            ax1.set_xlabel('Category')
            ax1.set_ylabel('Amount / £')
            ax1.set_title(f'Category-wise Spending for {month} {year}')
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=360, ha='center')

            # Monthly deposit for the year
            monthly_deposit = df[df['Category'] == 'MONTHLY DEPOSIT!']
            monthly_summary = monthly_deposit.groupby(df['Date'].dt.month)['Total'].sum()
            monthly_summary.plot(kind='line', ax=ax2)
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Amount / £')
            ax2.set_title(f'Deposit Amount per Month for {year}')
            ax2.set_xticks(range(1, 13))

            # Saved per month for the year
            saved = monthly_deposit.groupby(df['Date'].dt.month)['Available'].sum()
            saved.plot(kind='line', ax=ax3)
            ax3.set_xlabel('Month')
            ax3.set_ylabel('Amount / £')
            ax3.set_title(f'Available Amount per Month for {year}')
            ax3.set_xticks(range(1, 13))

            # Spent per month for the year
            both_totals = monthly_deposit.groupby(df['Date'].dt.month)[['Total', 'Available']].sum()
            spent = both_totals['Total'] - both_totals['Available']
            spent.plot(kind='line', ax=ax4)
            ax4.set_xlabel('Month')
            ax4.set_ylabel('Amount / £')
            ax4.set_title(f'Spent per Month for {year}')
            ax4.set_xticks(range(1, 13))

            fig_name = f"{year} summary.png"
            plt.savefig(fig_name)

            folder_name = f"{year}"
            upload(folder_name, fig_name)

            show_message(message_label, text=f"Yearly Summary for {year}\nSuccessfully Generated!", colour='green')
            logging.info(f"{year} Yearly summary generated successfully!")

        else:
            show_message(message_label, text=f"Check {year} data!", colour="red")
            logging.info(f"{month} {year} doesn't have values to create a dataframe")


def centered(window: tk.Tk, width: int, height: int) -> None:
    """
    Center a Tkinter window on the screen.

    Parameters:
        window (tk.Tk): The Tkinter window to be centered.
        width (int): The desired width of the window.
        height (int): The desired height of the window.
    """
    try:
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
        centered_width, centered_height = (screen_width - width) // 2, (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{centered_width}+{centered_height}")
    except TypeError as error:
        print(f"An Error occurred: {error}")


def gui() -> None:
    """
    Main function for GUI representation

    Returns:
        None: This function does not return a value but displays everything
    """
    # Creating and main window operations
    logging.info("Program Started!")
    window = tk.Tk()
    window.title("EXPENSE'S SHEET")

    style = ThemedStyle(window)
    style.set_theme("kroc")
    # pprint.pprint(style.theme_names())
    centered(window, 500, 700)
    main_frame = tk.Frame(window)
    main_frame.pack(fill='both', expand=1)
    create_database()

    canvas = tk.Canvas(main_frame)
    vsb = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    hsb = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')
    canvas.pack(side='left', fill='both', expand=1)

    canvas.update_idletasks()  # update canvas to get correct dimensions
    canvas_width = canvas.winfo_width()
    # canvas_height = canvas.winfo_height()
    x = canvas_width // 2

    content_frame = tk.Frame(canvas)
    window_id = canvas.create_window((x, 0), window=content_frame, anchor="n")

    def on_canvas_resize(event):
        """
        Readjusts the canvas position

        Args:
            event: gets the current width from the canvas window
        """
        canvas_width = event.width
        # canvas_height = event.height
        x = canvas_width // 2
        canvas.coords(window_id, x, 0)

    # Update scrollregion whenever content_frame is resized
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Update canvas whenever its resized
    canvas.bind("<Configure>", on_canvas_resize)

    window_label = tk.Label(content_frame, text="Welcome To Expense Tracker!", font=("Quicksand", 25, "italic"))
    window_label.pack(pady=20)
    # Main listbox operations
    Operations = ["Add Amount", "Deduct Amount", "View Sheet", "Delete", "Convert", "Summary"]
    values = tk.StringVar()
    Operations_label = tk.Label(content_frame, text="Select a Task: ", font=("Quicksand", 15, "italic"))
    Operations_box = ttk.Combobox(content_frame, textvariable=values, font=("Quicksand", 15, "italic"))
    Operations_box['values'] = Operations
    Operations_box['state'] = 'readonly'
    Operations_label.pack(pady=5)
    Operations_box.pack()
    global_message_label = tk.Label(content_frame, text="", font=("Quicksand", 15, "italic"))

    # Deposit fields
    deposit_frame = tk.Frame(content_frame)
    deposit_label = tk.Label(deposit_frame, text="Enter Your Deposit Amount: ", font=("Quicksand", 17, "italic"))
    deposit_value = tk.DoubleVar()
    deposit_date_label = tk.Label(deposit_frame, text="Select a Date for deposit: ", font=("Quicksand", 17, "italic"))
    deposit_calendar = Calendar(deposit_frame, date_pattern="y-mm-dd")
    # Create a Label to display the pound symbol (£)
    pound_label = tk.Label(deposit_frame, text="£", font=("Quicksand", 15))
    deposit_entry = ttk.Spinbox(
        deposit_frame,
        from_=0,
        to=9999999999999,
        textvariable=deposit_value,
        wrap=False,  # Dont want user to go over the limit
        increment=0.01,
        font=("Quicksand", 15)
    )
    deposit_button = tk.Button(
        deposit_frame,
        text="Deposit",
        command=lambda: deposit(deposit_calendar, deposit_entry.get(), global_message_label, toggle_deposit),
        font=("Quicksand", 15, "bold")
    )

    # Deduction fields
    deduction_frame = tk.Frame(content_frame)
    Categories = ["", "Food", "Entertainment", "Business", "Shopping", "Misc", "Other"]
    deduct_label_category = tk.Label(deduction_frame, text="Select a category: ", font=("Quicksand", 17, "italic"))
    Category = tk.StringVar()
    deduction_box = ttk.Combobox(deduction_frame, textvariable=Category, font=("Quicksand", 15, "italic"))
    deduction_box['values'] = Categories
    deduction_box['state'] = 'readonly'
    deduct_cal_label = tk.Label(deduction_frame, text="Select a date: ", font=("Quicksand", 15, "italic"))
    deduction_calendar = Calendar(deduction_frame, date_pattern="y-mm-dd")
    deduction_description = tk.Label(deduction_frame, text="Enter a description: ", font=("Quicksand", 17, "italic"))
    deduction_entry_description = tk.Entry(deduction_frame, font=("Quicksand", 15, "italic"))
    pound_label_deduct = tk.Label(deduction_frame, text="£", font=("Quicksand", 17))
    deduction_value = tk.DoubleVar()
    deduction_value_label = tk.Label(deduction_frame, text="Enter amount to deduct: ", font=("Quicksand", 17, "italic"))
    deduction_entry_value = ttk.Spinbox(
        deduction_frame,
        from_=0,
        to=9999999999999,
        textvariable=deduction_value,
        wrap=False,  # Dont want user to go over the limit
        increment=0.01,
        font=("Quicksand", 15)
    )
    deduct_button = tk.Button(deduction_frame, text="Deduct",
                              command=lambda: deduct(deduction_calendar, deducted_Category,
                                                     deduction_entry_description.get(),
                                                     deduction_entry_value.get(),
                                                     global_message_label,
                                                     toggle_deduct),
                              font=("Quicksand", 15, "bold"))
    view_frame = tk.Frame(content_frame)

    # View fields
    view_label_date = tk.Label(view_frame, text="Select a Month: ", font=("Quicksand", 15, "italic"))
    view_dates = Calendar(view_frame, date_pattern="y-mm-dd")
    view_box = scrolledtext.ScrolledText(view_frame, wrap=tk.WORD, width=80, height=20)
    view_button = tk.Button(view_frame, text="View", command=lambda: view(view_dates, global_message_label, view_box),
                            font=("Quicksand", 15, "bold"))

    # Convert fields
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    years = [str(year) for year in range(2000, 2050)]
    month_val = tk.StringVar()
    year_val = tk.StringVar()
    convert_frame = tk.Frame(content_frame)
    month_label = tk.Label(convert_frame, text="Select a month: ", font=("Quicksand", 15, "italic"))
    month_box = ttk.Combobox(convert_frame, textvariable=month_val, font=("Quicksand", 15, "italic"))
    current_month = datetime.date.today().strftime('%B')
    month_box.set(current_month)
    month_box['values'] = months
    month_box['state'] = 'readonly'
    year_label = tk.Label(convert_frame, text="Select a year: ", font=("Quicksand", 15, "italic"))
    year_box = ttk.Combobox(convert_frame, textvariable=year_val, font=("Quicksand", 15, "italic"))
    current_year = datetime.date.today().year
    year_box.set(str(current_year))
    year_box['values'] = years
    year_box['state'] = 'readonly'

    convert_label = tk.Label(convert_frame, text="Select conversion method: ", font=("Quicksand", 17, "italic"))
    conversions = ['Excel', 'Pandas', 'CSV', 'Bar Graph', 'Pie Chart', 'Line Chart', 'Histogram']
    convert_selection = tk.StringVar()
    convert_main_box = ttk.Combobox(convert_frame, textvariable=convert_selection, font=("Quicksand", 15, "italic"))
    convert_main_box['values'] = conversions
    convert_main_box['state'] = 'readonly'

    convert_button = tk.Button(convert_frame, text="Convert", command=lambda: convert(convert_selection.get(),
                                                                                      get_month_year,
                                                                                      global_message_label),
                               font=("Quicksand", 15, "bold"))

    # Delete fields
    delete_frame = tk.Frame(content_frame)
    Categories = ["", "Food", "Entertainment", "Business", "Shopping", "Misc", "Other", "MONTHLY DEPOSIT!"]
    delete_label_category = tk.Label(delete_frame, text="Select a category: ", font=("Quicksand", 17, "italic"))
    Category_delete = tk.StringVar()
    deletion_box = ttk.Combobox(delete_frame, textvariable=Category_delete, font=("Quicksand", 15, "italic"))
    deletion_box['values'] = Categories
    deletion_box['state'] = 'readonly'
    delete_label = tk.Label(delete_frame, text="Select a date to delete: ", font=("Quicksand", 15, "italic"))
    delete_calendar = Calendar(delete_frame, date_pattern="y-mm-dd")
    delete_button = tk.Button(delete_frame, text="Delete",
                              command=lambda: delete(delete_calendar, deleted_Category, global_message_label,
                                                     toggle_delete),
                              font=("Quicksand", 15, "bold"))

    # Summary fields
    summary_frame = tk.Frame(content_frame)
    summary_label = tk.Label(summary_frame, text="Select a summary option: ", font=("Quicksand", 15, "italic"))
    summary_options = ["Monthly", "Yearly"]
    summary_value = tk.StringVar()
    summary_box = ttk.Combobox(summary_frame, textvariable=summary_value, font=("Quicksand", 15, "italic"))
    summary_box['values'] = summary_options
    summary_box['state'] = 'readonly'
    summary_month_label = tk.Label(summary_frame, text="Select a month: ", font=("Quicksand", 15, "italic"))
    summary_month_box = ttk.Combobox(summary_frame, textvariable=month_val, font=("Quicksand", 15, "italic"))
    summary_current_month = datetime.date.today().strftime('%B')
    summary_month_box.set(summary_current_month)
    summary_month_box['values'] = months
    summary_month_box['state'] = 'readonly'
    summary_year_label = tk.Label(summary_frame, text="Select a year: ", font=("Quicksand", 15, "italic"))
    summary_year_box = ttk.Combobox(summary_frame, textvariable=year_val, font=("Quicksand", 15, "italic"))
    summary_current_year = datetime.date.today().year
    summary_year_box.set(str(summary_current_year))
    summary_year_box['values'] = years
    summary_year_box['state'] = 'readonly'
    # summary_box.set('Monthly')
    summary_button = tk.Button(summary_frame, text="Summary",
                               command=lambda: summary(summary_value.get(), get_month_year,
                                                       global_message_label, toggle_summary),
                               font=("Quicksand", 15, "italic"))

    def deducted_Category(event=None) -> str:
        """Toggles state of the category combobox

        Returns:
            the selected or inputted category!
        """
        logging.info("Getting Category!")
        if Category.get() == "Other":
            deduct_label_category.config(text="Enter Your Category: ")
            deduction_box.config(state='normal')
        else:
            deduction_box.config(state='readonly')
        return Category.get()

    def deleted_Category(event=None) -> str:
        """Toggles state of the category combobox

        Returns:
            the selected or inputted category!
        """
        logging.info("Getting Category!")
        if Category_delete.get() == "Other":
            deduct_label_category.config(text="Enter Your Category: ")
            deduction_box.config(state='normal')
        else:
            deduction_box.config(state='readonly')
        return Category_delete.get()

    def get_month_year() -> tuple[str, str]:
        """
        Gets Month and Year from the year and month box

        Returns:
            month and year from the chosen month & year box
        """
        logging.info("getting month and year from month and year box")
        selected_month = month_val.get()
        selected_year = year_val.get()
        return selected_month, selected_year

    def toggle_deposit(enable) -> None:
        """
        Toggles deposit fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling deposit fields!")
            deposit_date_label.grid(row=0, column=1, pady=10)
            deposit_calendar.grid(row=1, column=1, pady=10)
            deposit_label.grid(row=2, column=1, pady=10)
            pound_label.grid(row=3, column=0, padx=2)
            deposit_entry.grid(row=3, column=1)
            deposit_button.grid(row=4, column=1, columnspan=2, pady=10)
            deposit_frame.pack()
        else:
            deposit_entry.delete(0, tk.END)
            deposit_frame.pack_forget()

    def toggle_deduct(enable) -> None:
        """
        Toggles deduct fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling deduct fields!")
            deduct_label_category.grid(row=0, column=1)
            deduction_box.grid(row=1, column=1, pady=5)
            deducted_Category()
            deduct_cal_label.grid(row=2, column=1)
            deduction_calendar.grid(row=3, column=1, pady=10)
            deduction_description.grid(row=4, column=1)
            deduction_entry_description.grid(row=5, column=1, pady=5)
            deduction_value_label.grid(row=6, column=1, pady=10)
            pound_label_deduct.grid(row=7, column=0, padx=2, pady=5)
            deduction_entry_value.grid(row=7, column=1, pady=5)
            deduct_button.grid(row=8, column=0, columnspan=2, pady=10)
            deduction_frame.pack()
        else:
            deduction_entry_description.delete(0, tk.END)
            deduction_entry_value.delete(0, tk.END)
            deduction_box.set(Categories[0])
            deduction_frame.pack_forget()

    def toggle_view(enable) -> None:
        """
        Toggles view fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling view fields!")
            view_box.delete("1.0", tk.END)
            view_label_date.grid(row=0, column=0, pady=10)
            view_dates.grid(row=1, column=0, pady=10)
            view_button.grid(row=2, column=0, columnspan=2, pady=10)
            view_box.config(state='normal')
            view_box.tag_configure("custom_font", font=("Quicksand", 15), foreground="black")
            view_frame.pack()
        else:
            view_frame.pack_forget()

    def toggle_convert(enable) -> None:
        """
        Toggles convert fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling convert fields!")
            convert_label.grid(row=0, column=0, pady=5)
            convert_main_box.grid(row=1, column=0, pady=5)
            month_label.grid(row=2, column=0, pady=5)
            month_box.grid(row=3, column=0, pady=5)
            year_label.grid(row=4, column=0, pady=5)
            year_box.grid(row=5, column=0, pady=5)
            convert_button.grid(row=6, column=0, columnspan=2, pady=5)
            convert_frame.pack()
        else:
            convert_frame.pack_forget()

    def toggle_delete(enable) -> None:
        """
        Toggles delete fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling delete fields!")
            delete_label.grid(row=0, column=0, pady=5)
            delete_calendar.grid(row=1, column=0, pady=5)
            delete_label_category.grid(row=2, column=0, pady=5)
            deletion_box.grid(row=3, column=0, pady=5)
            deleted_Category()
            delete_button.grid(row=4, column=0, columnspan=2, pady=10)
            delete_frame.pack()
        else:
            delete_frame.pack_forget()

    def get_summary(event=None) -> None:
        """
        Gets the value from the summary combobox

        Returns:
            None: Does not return anything but displays fields
        """
        selection = summary_box.get()
        if selection == 'Monthly':
            logging.info("Monthly summary fields displayed!")
            summary_month_label.grid(row=2, column=0, pady=5)
            summary_month_box.grid(row=3, column=0, pady=10)
            summary_year_label.grid(row=4, column=0, pady=5)
            summary_year_box.grid(row=5, column=0, pady=10)
            summary_button.grid(row=6, column=0, columnspan=2, pady=10)
            summary_frame.pack()
        elif summary_value.get() == 'Yearly':
            logging.info("Yearly summary fields displayed!")
            summary_month_label.grid_forget()
            summary_month_box.grid_forget()
            summary_year_label.grid(row=2, column=0, pady=5)
            summary_year_box.grid(row=3, column=0, pady=10)
            summary_button.grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_summary(enable):
        """
        Toggles summary function fields

        Returns:
            None: Does not return anything but displays fields
        """
        if enable:
            logging.info("Toggling summary fields!")
            summary_label.grid(row=0, column=0, pady=10)
            summary_box.grid(row=1, column=0, pady=5)
            summary_frame.pack()
        else:
            summary_frame.pack_forget()

    def get_value(event) -> None:
        """
        Gets the value from the main combobox

        Returns:
            None: Does not return anything but displays fields
        """
        task = values.get()
        if task == 'Add Amount':
            toggle_deposit(True)
            toggle_deduct(False)
            toggle_view(False)
            toggle_convert(False)
            toggle_delete(False)
            toggle_summary(False)
        elif task == 'Deduct Amount':
            toggle_deduct(True)
            toggle_deposit(False)
            toggle_view(False)
            toggle_convert(False)
            toggle_delete(False)
            toggle_summary(False)
        elif task == 'View Sheet':
            toggle_view(True)
            toggle_deposit(False)
            toggle_deduct(False)
            toggle_convert(False)
            toggle_delete(False)
            toggle_summary(False)
        elif task == 'Convert':
            toggle_convert(True)
            toggle_deposit(False)
            toggle_deduct(False)
            toggle_view(False)
            toggle_delete(False)
            toggle_summary(False)
        elif task == 'Delete':
            toggle_delete(True)
            toggle_deposit(False)
            toggle_deduct(False)
            toggle_view(False)
            toggle_convert(False)
            toggle_summary(False)
        elif task == 'Summary':
            toggle_summary(True)
            toggle_delete(False)
            toggle_deposit(False)
            toggle_deduct(False)
            toggle_view(False)
            toggle_convert(False)

    Operations_box.bind('<<ComboboxSelected>>', get_value)
    deduction_box.bind("<<ComboboxSelected>>", deducted_Category)
    summary_box.bind("<<ComboboxSelected>>", get_summary)

    entry_mappings = {
        deposit_entry: deposit_calendar,
        deposit_calendar: deposit_button,
        deduction_box: deduction_entry_description,
        deduction_entry_description: deduction_entry_value,
        deduction_entry_value: deduct_button,
        convert_main_box: month_box,
        month_box: year_box,
        delete_calendar: delete_button,
        summary_box: summary_month_box,
        summary_month_box: summary_year_box,
        summary_year_box: summary_button,
    }

    def widget_handler(event) -> None:
        """
        Gets the focus of the widgets and sets focus of the next

        Returns:
            None: Does not return anything but focuses and invokes fields and button
        """
        logging.info("widget handler called!")
        current = window.focus_get()
        for widget, next_widget in entry_mappings.items():
            if widget == current:
                next_widget.focus()
                break
        for button in [deposit_button, deduct_button, delete_button]:
            if current == button:
                button.invoke()
        view_button.focus_set()
        convert_button.focus_set()
        summary_button.focus_set()

    for widgets in entry_mappings:
        widgets.bind("<Return>", widget_handler)
    for buttons in [deposit_button, deduct_button, view_button, convert_button, delete_button, summary_button]:
        buttons.bind("<Return>", widget_handler)

    # Closes the Application
    def close() -> None:
        """
        Closes the application

        Returns:
            None: Does not return anything but displays the messagebox
        """
        logging.info("Closing the application!")
        if messagebox.askyesno(title="EXIT", message="Do You Wanna Quit? "):
            window.destroy()
            messagebox.showinfo(message="EXITED SUCCESSFULLY")

    window.protocol("WM_DELETE_WINDOW", close)
    window.mainloop()


def logging_function() -> None:
    """Creates a console and file logging handler that logs messages
        Returns:
              None: Returns nothing but calls the logging function
    """
    logging.basicConfig(level=logging.INFO, format='%(funcName)s --> %(message)s : %(asctime)s - %(levelname)s',
                        datefmt="%d-%m-%Y %I:%M:%S %p")

    File_handler = logging.FileHandler('Expenses.log')
    File_handler.setLevel(level=logging.WARNING)
    Format = logging.Formatter('%(funcName)s --> %(message)s : %(asctime)s - %(levelname)s',
                               "%d-%m-%Y %I:%M:%S %p")
    File_handler.setFormatter(Format)

    Logger = logging.getLogger('')
    Logger.addHandler(File_handler)


if __name__ == '__main__':
    logging_function()
    gui()
