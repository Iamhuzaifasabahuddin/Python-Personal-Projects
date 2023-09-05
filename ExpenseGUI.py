import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3


def show_message(message_label, text, colour, duration=2000):
    message_label.config(text=text, fg=colour)
    message_label.pack(pady=10)
    message_label.after(duration, command=lambda: message_label.pack_forget())


def deposit(value, message_label, toggle_deposit):
    show_message(message_label, text=f"Hello with {value}", colour='green')


def deduct():
    raise NotImplementedError


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

    main_frame = tk.Frame(centered(window, 500, 500))
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
    deposit_message_label = tk.Label(main_frame, text="", font=("Quicksand", 15, "italic"))
    deposit_button = tk.Button(
        deposit_frame,
        text="Deposit",
        command=lambda: deposit(deposit_entry.get(), deposit_message_label, toggle_deposit),
        font=("Quicksand", 15, "bold")
    )

    def toggle_deposit(enable):
        if enable:
            deposit_label.pack(pady=10)
            pound_label.grid(row=0, column=0, padx=5)
            deposit_entry.grid(row=0, column=1)
            deposit_button.grid(row=1, column=0, columnspan=2, pady=10)  # Center-align the button
            deposit_frame.pack()
        else:
            deposit_label.pack_forget()
            pound_label.pack_forget()
            deposit_entry.pack_forget()
            deposit_frame.pack_forget()

    def get_value(event):
        task = values.get()
        if task == 'Add Amount':
            toggle_deposit(True)
        elif task == 'Deduct Amount':
            pass
        elif task == 'View Sheet':
            pass
        elif task == 'Convert':
            pass

    Operations_box.bind('<<ComboboxSelected>>', get_value)
    window.mainloop()


if __name__ == '__main__':
    gui()
