import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3
import logging


def show_message(message_label, text, colour, duration=2000):
    message_label.config(text=text, fg=colour)
    message_label.pack(pady=10)
    message_label.after(duration, lambda: message_label.pack_forget())


def deposit(value, message_label, toggle_deposit):
    try:
        connection = sqlite3.connect('Expenses.db')
        cursor = connection.cursor()
        today = datetime.date.today()
        formatted_date = today.strftime('%Y-%m')
        value = float(value)
        if value <= 0:
            show_message(message_label, text="Amount should be greater than 0!", colour="red")
            logging.info(f"Invalid Input!")
        else:
            cursor.execute("SELECT Available FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                           (formatted_date, "MONTHLY DEPOSIT!"))
            existing_total = cursor.fetchone()
            if existing_total:
                existing_total = existing_total[0]
                new_total = existing_total + value
                # Update the existing deposit record
                cursor.execute("UPDATE Transactions SET Amount = ?, Available = ?, Description=? "
                               "WHERE strftime('%Y-%m', Date) = ? AND "
                               "Category = ?",
                               (value, new_total, "Updated Deposit!", formatted_date, "MONTHLY DEPOSIT!"))
            else:
                cursor.execute("INSERT INTO Transactions (Date, Category, Amount, Available) VALUES (?, ?, ?, ?)",
                               (today.strftime('%Y-%m-%d'), "MONTHLY DEPOSIT!", value, value))
            show_message(message_label,
                         text=f"Deposit for month: {today.strftime('%B')}\nValue: £{value} is Successful!\n"
                              f"Current balance: £{existing_total}\nUpdated balance £{new_total}",
                         colour="green", duration=3000)
            connection.commit()
            toggle_deposit(False)
            logging.info("Successfully deposited the amount!")
    except (ValueError, sqlite3.Error) as error:
        show_message(message_label, text=f"Invalid Value Entered", colour="red")
        logging.info(f"ERROR: {error}!")


def deduct(category, description, value, message_label, toggle_deduct):
    try:
        option = category()
        today = datetime.date.today()
        formatted_date = today.strftime('%Y-%m')
        value = float(value)

        connection = sqlite3.connect("Expenses.db")
        cursor = connection.cursor()
        # Fetch the existing total deposit for the current month
        cursor.execute("SELECT Available FROM Transactions WHERE strftime('%Y-%m', Date) = ? AND Category = ?",
                       (formatted_date, "MONTHLY DEPOSIT!"))
        existing_total = cursor.fetchone()
        if value <= 0 or option.strip() == "":
            show_message(message_label, text="Invalid Entry!\n(check value > 0 & category is not empty)", colour="red")
            logging.info("Value should be greater than 0! or Category is empty")
        else:
            if existing_total is None:
                show_message(message_label, text=f"No deposit made for the month {today.strftime('%B')}", colour="red")
                logging.info("No funds allocated for the month!")
            else:
                existing_total = existing_total[0]
                if value > existing_total:
                    show_message(message_label, text="Insufficient Funds!", colour="red")
                    logging.info("Insufficient funds in the database add more!")
                else:
                    new_total = existing_total - value
                    if description.strip() == "":
                        description = "N/A"
                    # Entering main category to db
                    cursor.execute("INSERT INTO Transactions (Date, Category, Description, Amount, Available) "
                                   "VALUES (?, ?, ?, ?, ?)",
                                   (today.strftime('%Y-%m-%d'), option, description, value, new_total))
                    # Updating Available in db
                    cursor.execute("UPDATE Transactions SET Available = ? WHERE strftime('%Y-%m', Date) = ?",
                                   (new_total, formatted_date))
                    # Updating Every Available column in db
                    cursor.execute("UPDATE Transactions SET Available = ? WHERE strftime('%Y-%m', Date) = ? AND "
                                   "Category = ?",
                                   (new_total, formatted_date, "MONTHLY DEPOSIT!"))
                    show_message(message_label, text="Success!", colour='green')
                    logging.info("Successfully Inserted & Updated the data into the database")
            connection.commit()
            connection.close()
    except (ValueError, TypeError, sqlite3.Error) as error:
        show_message(message_label, text=f"{error}", colour='red')
        logging.info(f"ERROR: {error}!")


def convert():
    raise NotImplementedError


def view():
    raise NotImplementedError


def centered(window, width, height):
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
    window_label.pack(pady=10)
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
        command=lambda: deposit(deposit_entry.get(), global_message_label, toggle_deposit),
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
                                                                                     deduction_entry_value.get(),
                                                                                     global_message_label,
                                                                                     toggle_deduct),
                              font=("Quicksand", 15, "bold"))

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

    def get_value(event):
        task = values.get()
        if task == 'Add Amount':
            toggle_deposit(True)
            toggle_deduct(False)
        elif task == 'Deduct Amount':
            toggle_deposit(False)
            toggle_deduct(True)
        elif task == 'View Sheet':
            pass
        elif task == 'Convert':
            pass

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
    Operations_box.bind('<<ComboboxSelected>>', get_value)
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
