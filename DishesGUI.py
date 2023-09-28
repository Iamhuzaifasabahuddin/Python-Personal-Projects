import logging
import pprint
import tkinter as tk
from typing import Callable

from ttkthemes import ThemedStyle
from tkinter import ttk, scrolledtext, messagebox


def show_message(message_label: tk.Label, text: str, colour: str, duration: int = 2000):
    """
           Display a message on the GUI.

           Args:
               message_label (tk.Label): The label widget to display the message.
               text (str): The message text.
               colour (str): The color of the message text.
               duration (int, optional): Duration in milliseconds to display the message. Default is 2000ms.
           """
    message_label.config(text=text, fg=colour)
    message_label.pack()
    message_label.after(duration, lambda: message_label.pack_forget())


def dishes(ingredient: str, message_label: tk.Label, listbox: tk.scrolledtext.ScrolledText, toggle_recipes: Callable):
    listbox.insert(tk.END, ingredient, "custom_font")
    listbox.after(2500, listbox.grid(row=3, column=1, pady=5))


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
    """Displays the GUI element"""
    logging.info("Starting GUI...")
    window = tk.Tk()
    window.title("Dishes App")
    centered(window, 500, 700)
    style = ThemedStyle(window)
    pprint.pprint(style.theme_names())
    style.set_theme('arc')
    main_frame = tk.Frame(window)
    main_frame.pack(fill='both', expand=1)

    canvas = tk.Canvas(main_frame)

    vsb = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    hsb = tk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
    canvas.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

    vsb.pack(fill='y', side='right')
    hsb.pack(fill='x', side='bottom')
    canvas.pack(side='left', fill='both', expand=1)

    canvas.update_idletasks()
    canvas_width = canvas.winfo_width()
    x = canvas_width // 2

    content_frame = tk.Frame(canvas)
    window_id = canvas.create_window((x, 0), window=content_frame, anchor="n")

    def update(event):
        updated_width = event.width
        new_width = updated_width // 2
        canvas.coords(window_id, new_width, 0)

    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind("<Configure>", update)

    main_title = tk.Label(content_frame, text="Welcome To Recipe Generator!", font=("Quicksand", 25, "italic"))
    main_title.pack(pady=10)

    global_message_label = tk.Label(content_frame, text="", font=("Quicksand", 15, "italic"))
    recipe_frame = tk.Frame(content_frame)
    recipe_title = tk.Label(recipe_frame, text="Enter an ingredient: ", font=("Quicksand", 15, "italic"))
    recipe_entry = tk.Entry(recipe_frame, font=("Quicksand", 15, "italic"))
    recipe_box = scrolledtext.ScrolledText(recipe_frame, wrap=tk.WORD, width=80, height=20)
    recipe_button = tk.Button(recipe_frame, text="Fetch", font=("Quicksand", 15, "bold"),
                              command=lambda: dishes(recipe_entry.get(),
                                                     global_message_label,
                                                     recipe_box, toggle_recipe))

    def toggle_recipe(enable):
        if enable:
            recipe_title.grid(row=0, column=1, pady=10)
            recipe_entry.grid(row=1, column=1, pady=5)
            recipe_button.grid(row=2, column=1, pady=15, columnspan=2)
            recipe_box.config(state='normal')
            recipe_box.tag_configure("custom_font", font=("Quicksand", 15), foreground="black")
            recipe_frame.pack()
        else:
            recipe_frame.pack_forget()

    toggle_recipe(True)

    def close() -> None:
        """
                Closes the application

                Returns:
                    None: Does not return anything but displays the messagebox
                """
        logging.info("Closing the application!")
        if messagebox.askyesno("Exit", "Are you sure you want to close?"):
            window.destroy()
            messagebox.showinfo("Closed", "Exited successfully!")

    entry_mapping = {
        recipe_entry: recipe_button
    }

    def widget_handler(event):
        logging.info("Widget handler called...")
        current = window.focus_get()
        for widget, next_widget in entry_mapping.items():
            if widget == current:
                next_widget.focus()
                break
        for button in [recipe_button]:
            if button == current:
                button.invoke()

    for widgets in entry_mapping:
        widgets.bind("<Return>", widget_handler)
    for buttons in [recipe_button]:
        buttons.bind("<Return>", widget_handler)
    window.protocol("WM_DELETE_WINDOW", close)
    window.mainloop()


def logging_funtion() -> None:
    logging.basicConfig(level=logging.INFO, format="%(funcName)s --> %(message)s : %(asctime)s - %(levelname)s",
                        datefmt=
                        "%d-%m-%Y %I:%M:%S %p")

    filehandler = logging.FileHandler('Recipe_generator.log')
    filehandler.setLevel(logging.WARNING)
    Format = logging.Formatter('%(funcName)s --> %(message)s : %(asctime)s - %(levelname)s',
                               "%d-%m-%Y %I:%M:%S %p")
    filehandler.setFormatter(Format)

    logger = logging.getLogger('')
    logger.addHandler(filehandler)


if __name__ == '__main__':
    logging_funtion()
    gui()
