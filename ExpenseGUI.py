import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import Calendar
import sqlite3
import logging
from typing import Callable


def show_message(message_label: tk.Label, text: str, colour: str, duration=2000):
    message_label.config(text=text, fg=colour)
    message_label.pack(pady=10)
    message_label.after(duration, lambda: message_label.pack_forget())


def deposit(value: float, message_label: tk.Label, toggle_deposit: Callable):
    try:
        connection = sqlite3.connect('Expenses.db')
        cursor = connection.cursor()
        today = datetime.date.today()
        formatted_date = today.strftime('%Y-%m')
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
                    (today.strftime('%Y-%m-%d'), value, new_available, new_total, formatted_date, "MONTHLY DEPOSIT!"))
                # Update Available and Total columns
                cursor.execute("UPDATE Transactions SET Available = ?, Total = ? WHERE strftime('%Y-%m', Date) = ?",
                               (new_available, new_total, formatted_date))
            else:
                # Insert a new deposit record
                cursor.execute("INSERT INTO Transactions (Date, Category, Amount, Available, Total) VALUES (?, ?, ?, "
                               "?, ?)",
                               (today.strftime('%Y-%m-%d'), "MONTHLY DEPOSIT!", value, value, value))
            show_message(message_label,
                         text=f"Deposit for month: {today.strftime('%B')}\nValue: £{value} is Successful!\n"
                              f"Current balance: £{new_available}\nTotal amount deposited: £{new_total}",
                         colour="green", duration=3000)
            connection.commit()
            connection.close()
            # toggle_deposit(False)
            logging.info("Successfully deposited the amount!")
    except (ValueError, sqlite3.Error) as error:
        show_message(message_label, text=f"Invalid Value Entered", colour="red")
        logging.info(f"ERROR: {error}!")


def deduct(category: Callable, description: str, value: float, message_label: tk.Label, toggle_deduct: Callable):
    try:
        option = category()
        today = datetime.date.today()
        formatted_date = today.strftime('%Y-%m')

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
                show_message(message_label, text=f"No deposit made for the month {today.strftime('%B')}", colour="red")
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
                                   (today.strftime('%Y-%m-%d'), option, description, value,
                                    new_available, existing_total))
                    # Updating Available in db
                    cursor.execute("UPDATE Transactions SET Available = ? WHERE strftime('%Y-%m', Date) = "
                                   "? AND Category = ?",
                                   (new_available, formatted_date, "MONTHLY DEPOSIT!"))
                    # Updating Every Available column in db
                    cursor.execute("UPDATE Transactions SET Available = ? WHERE strftime('%Y-%m', Date) = ?",
                                   (new_available, formatted_date))
                    show_message(message_label, text="Success!", colour='green')
                    logging.info("Successfully Inserted & Updated the data into the database")
            connection.commit()
            connection.close()
    except (ValueError, TypeError, sqlite3.Error) as error:
        show_message(message_label, text=f"{error}", colour='red')
        logging.info(f"ERROR: {error}!")


def convert():
    raise NotImplementedError


def view(date, message_label):
    dated = date.get_displayed_month()
    show_message(message_label, text=f"{dated}", colour="green")


def centered(window: tk.Tk, width: int, height: int):
    try:
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
        centered_width, centered_height = (screen_width - width) // 2, (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{centered_width}+{centered_height}")
    except TypeError as error:
        print(f"An Error occurred {error}")


def gui():
    # Creating and main window operations
    window = tk.Tk()
    window.title("EXPENSE'S SHEET")

    main_frame = tk.Frame(centered(window, 700, 700))
    window_label = tk.Label(main_frame, text="Welcome To Expense Tracker!", font=("Quicksand", 25, "italic"))
    window_label.pack(pady=20)
    main_frame.pack(anchor="center")

    # Main listbox operations
    Operations = ["Add Amount", "Deduct Amount", "View Sheet", "Convert"]
    values = tk.StringVar()
    Operations_label = tk.Label(main_frame, text="Select a Task: ", font=("Quicksand", 15, "italic"))
    Operations_box = ttk.Combobox(main_frame, textvariable=values, font=("Quicksand", 15, "italic"))
    Operations_box['values'] = Operations
    Operations_box['state'] = 'readonly'
    Operations_label.pack(pady=5)
    Operations_box.pack()
    global_message_label = tk.Label(main_frame, text="", font=("Quicksand", 15, "italic"))

    # Deposit fields
    deposit_label = tk.Label(main_frame, text="Enter Your Deposit Amount: ", font=("Quicksand", 17, "italic"))
    deposit_value = tk.DoubleVar()
    # Create a Frame to hold the pound symbol (£) and the entry field
    deposit_frame = tk.Frame(main_frame)
    # Create a Label to display the pound symbol (£)
    pound_label = tk.Label(deposit_frame, text="£", font=("Quicksand", 15))
    deposit_entry = ttk.Spinbox(
        deposit_frame,
        from_=0,
        to=9999999999999,
        textvariable=deposit_value,
        wrap=True,
        increment=0.01,
        font=("Quicksand", 15)
    )
    deposit_button = tk.Button(
        deposit_frame,
        text="Deposit",
        command=lambda: deposit(float(deposit_entry.get()), global_message_label, toggle_deposit),
        font=("Quicksand", 15, "bold")
    )

    # Deduction fields
    deduction_frame = tk.Frame(main_frame)
    Categories = ["", "Food", "Entertainment", "Business", "Shopping", "Misc", "Other"]
    deduct_label_category = tk.Label(deduction_frame, text="Select a category: ", font=("Quicksand", 17, "italic"))
    Category = tk.StringVar()
    deduction_box = ttk.Combobox(deduction_frame, textvariable=Category, font=("Quicksand", 15, "italic"))
    deduction_box['values'] = Categories
    deduction_box['state'] = 'readonly'
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
        wrap=True,
        increment=0.01,
        font=("Quicksand", 15)
    )
    deduct_button = tk.Button(deduction_frame, text="Deduct", command=lambda: deduct(deducted_Category,
                                                                                     deduction_entry_description.get(),
                                                                                     float(deduction_entry_value.get()),
                                                                                     global_message_label,
                                                                                     toggle_deduct),
                              font=("Quicksand", 15, "bold"))

    # View fields
    view_frame = tk.Frame(main_frame)
    view_label_date = tk.Label(view_frame, text="Select a Month: ", font=("Quicksand", 15, "italic"))
    view_dates = Calendar(view_frame)
    view_box = scrolledtext.ScrolledText(view_frame, wrap=tk.WORD, width=60, height=40)

    view_button = tk.Button(view_frame, text="View", command=lambda: view(view_dates, global_message_label))

    def deducted_Category(event=None):
        if Category.get() == "Other":
            deduct_label_category.config(text="Enter Your Category: ")
            deduction_box.config(state='normal')
        else:
            deduction_box.config(state='readonly')
        return Category.get()

    deduction_box.bind("<<ComboboxSelected>>", deducted_Category)

    def toggle_deposit(enable):
        if enable:
            deposit_label.pack(pady=10)
            pound_label.grid(row=0, column=0, padx=5)
            deposit_entry.grid(row=0, column=1)
            deposit_button.grid(row=1, column=0, columnspan=2, pady=10)  # Center-align the button
            deposit_frame.pack()
        else:
            deposit_label.pack_forget()
            deposit_frame.pack_forget()

    def toggle_deduct(enable):
        if enable:
            deduct_label_category.grid(row=0, column=1, pady=10)
            deduction_box.grid(row=1, column=1, pady=5)
            deducted_Category()
            deduction_description.grid(row=2, column=1, pady=10)
            deduction_entry_description.grid(row=3, column=1, pady=5)
            deduction_value_label.grid(row=4, column=1, pady=10)
            pound_label_deduct.grid(row=5, column=0, padx=2, pady=5)
            deduction_entry_value.grid(row=5, column=1, pady=5)
            deduct_button.grid(row=6, column=0, columnspan=2, pady=10)
            deduction_frame.pack()

        else:
            deduction_entry_description.delete(0, tk.END)
            deduction_entry_value.delete(0, tk.END)
            deduction_box.set(Categories[0])
            deduction_frame.pack_forget()

    def toggle_view(enable):
        if enable:
            view_label_date.grid(row=0, column=0, pady=10)
            view_dates.grid(row=1, column=0, pady=10)
            view_button.grid(row=2, column=0, columnspan=2, pady=10)
            view_box.config(state='normal')
            view_frame.pack()

        else:
            view_frame.pack_forget()
            view_box.config(state='disabled')
    def get_value(event):
        task = values.get()
        if task == 'Add Amount':
            toggle_deposit(True)
            toggle_deduct(False)
        elif task == 'Deduct Amount':
            toggle_deposit(False)
            toggle_deduct(True)
        elif task == 'View Sheet':
            toggle_deposit(False)
            toggle_deduct(False)
            toggle_view(True)
        elif task == 'Convert':
            pass

    Operations_box.bind('<<ComboboxSelected>>', get_value)

    entry_mappings = {
        deposit_entry: deposit_button,
        deduction_box: deduction_entry_description,
        deduction_entry_description: deduction_entry_value,
        deduction_entry_value: deduct_button
    }

    def widget_handler(event):
        current = window.focus_get()
        for widget, next_widget in entry_mappings.items():
            if widget == current:
                next_widget.focus()
                break
        for button in [deposit_button, deduct_button]:
            if current == button:
                button.invoke()

    for widgets in entry_mappings:
        widgets.bind("<Return>", widget_handler)
    for buttons in [deposit_button, deduct_button]:
        buttons.bind("<Return>", widget_handler)

    # Closes the Application
    def close():
        if messagebox.askyesno(title="EXIT", message="Do You Wanna Quit? "):
            window.destroy()
            messagebox.showinfo(message="EXITED SUCCESSFULLY")

    window.protocol("WM_DELETE_WINDOW", close)
    window.mainloop()


def logging_function():
    logging.basicConfig(level=logging.INFO, format='%(funcName)s - %(message)s - %(asctime)s - %(levelname)s',
                        datefmt="%Y-%m-%d %I:%M:%S %p")

    File_handler = logging.FileHandler('Expenses.log')
    File_handler.setLevel(level=logging.WARNING)
    Format = logging.Formatter('%(funcName)s - %(message)s - %(asctime)s - %(levelname)s',
                               "%Y-%m-%d %I:%M:%S %p")
    File_handler.setFormatter(Format)

    Logger = logging.getLogger('')
    Logger.addHandler(File_handler)


if __name__ == '__main__':
    logging_function()
    gui()
