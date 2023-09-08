import datetime
import pprint
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from dateutil.relativedelta import relativedelta
from tkcalendar import Calendar
import sqlite3
import logging
from typing import Callable
from ttkthemes import ThemedStyle


def show_message(message_label: tk.Label, text: str, colour: str, duration=2000):
    message_label.config(text=text, fg=colour)
    message_label.pack(pady=10)
    message_label.after(duration, lambda: message_label.pack_forget())


def deposit(date: Calendar, value: str, message_label: tk.Label, toggle_deposit: Callable):
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
                             colour="green", duration=3000)
            else:
                # Insert a new deposit record
                cursor.execute("INSERT INTO Transactions (Date, Category, Amount, Available, Total) VALUES (?, ?, ?, "
                               "?, ?)",
                               (selected_date.strftime('%Y-%m-%d'), "MONTHLY DEPOSIT!", value, value, value))
                show_message(message_label,
                             text=f"Deposit for month: {selected_date.strftime('%B')}\nValue: £{value} is Successful!\n",
                             colour="green", duration=3000)
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
           toggle_deduct: Callable):
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


def convert():
    raise NotImplementedError


def view(date: Calendar, message_label: tk.Label, view_box: tk.scrolledtext.ScrolledText):
    try:
        selected_date = date.parse_date(date.get_date())
        connection = sqlite3.connect("Expenses.db")
        cursor = connection.cursor()

        # Calculate the start and end dates for the selected month
        start_date = selected_date.strftime('%Y-%m-%d')
        end_date = (selected_date + relativedelta(day=31)).strftime('%Y-%m-%d')

        results = cursor.execute(
            "SELECT Date, Category, Amount, Available, Total FROM Transactions WHERE Date BETWEEN ? AND ?"
            "ORDER BY Date",
            (start_date, end_date))

        data = results.fetchall()
        if not data:
            view_box.delete("1.0", tk.END)
            show_message(message_label, text=f"No results found for the month of {selected_date.strftime('%B %Y')}",
                         colour="red")
            logging.info(f"No matches found for the month of {selected_date.strftime('%B %Y')}")
            view_box.pack_forget()
        else:
            show_message(message_label, text="Getting results......", colour="green")
            logging.info(f"Match found! for the month of {selected_date.strftime('%B %Y')}")
            view_box.delete("1.0", tk.END)
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
                spent += amount
                available = row[3]
                total_deposit = row[4]

            view_box.insert(tk.END, f"\nTOTAL AVAILABLE: £{available}\nTOTAL SPENT: £{spent}\n"
                                    f"TOTAL DEPOSITED: £{total_deposit}", "custom_font")
            view_box.after(2500, lambda: view_box.grid(row=3, column=0))

        connection.close()
    except sqlite3.Error as error:
        show_message(message_label, text=f"SQLite error: {error}", colour="red")
        logging.error(f"SQLite error: {error}")
    except (TypeError, ValueError) as error:
        show_message(message_label, text=f"An error occurred: {error}", colour="red")
        logging.error(f"An error occurred: {error}")


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

    style = ThemedStyle(window)
    style.set_theme("kroc")
    # pprint.pprint(style.theme_names())
    centered(window, 500, 700)
    main_frame = tk.Frame()
    main_frame.pack(fill='both', expand=1)

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
    Operations = ["Add Amount", "Deduct Amount", "View Sheet", "Convert"]
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
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    years = [str(year) for year in range(2000, 2050)]
    month_val = tk.StringVar()
    year_val = tk.StringVar()

    month_box = ttk.Combobox(deposit_frame, textvariable=month_val, font=("Quicksand", 15, "italic"))
    month_box.set("January")
    month_box['values'] = months
    month_box['state'] = 'readonly'
    year_box = ttk.Combobox(deposit_frame, textvariable=year_val, font=("Quicksand", 15, "italic"))
    current_year = datetime.date.today().year
    year_box.set(str(current_year))
    year_box['values'] = years
    year_box['state'] = 'readonly'

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

    def deducted_Category(event=None):
        if Category.get() == "Other":
            deduct_label_category.config(text="Enter Your Category: ")
            deduction_box.config(state='normal')
        else:
            deduction_box.config(state='readonly')
        return Category.get()

    def get_month_year(event=None):
        selected_month = month_val.get()
        selected_year = year_val.get()
        return selected_month, selected_year

    # Bind the function to the Comboboxes
    month_box.bind("<<ComboboxSelected>>", get_month_year)
    year_box.bind("<<ComboboxSelected>>", get_month_year)
    deduction_box.bind("<<ComboboxSelected>>", deducted_Category)

    def toggle_deposit(enable):
        if enable:
            deposit_date_label.grid(row=0, column=1, pady=10)
            deposit_calendar.grid(row=1, column=1, pady=10)
            deposit_label.grid(row=2, column=1, pady=10)
            pound_label.grid(row=3, column=0, padx=2)
            deposit_entry.grid(row=3, column=1)
            deposit_button.grid(row=4, column=1, columnspan=2, pady=10)  # Center-align the button
            deposit_frame.pack()
        else:
            deposit_frame.pack_forget()
            deposit_entry.delete(0, tk.END)

    def toggle_deduct(enable):
        if enable:
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

    def toggle_view(enable):
        if enable:
            view_label_date.grid(row=0, column=0, pady=10)
            view_dates.grid(row=1, column=0, pady=10)
            view_button.grid(row=2, column=0, columnspan=2, pady=10)
            view_box.config(state='normal')
            view_box.tag_configure("custom_font", font=("Quicksand", 15), foreground="black")
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
        deposit_entry: deposit_calendar,
        deposit_calendar: deposit_button,
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
