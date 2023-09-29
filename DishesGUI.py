import json
import logging
from http import HTTPStatus
import tkinter as tk
from typing import Callable
import requests
from ttkthemes import ThemedStyle
from tkinter import ttk, scrolledtext, messagebox


def dishes(query: str, nums: int, message_label: tk.Label, listbox: tk.scrolledtext.ScrolledText,
           toggle_recipes: Callable):
    app_id = json.load(open("Edamam_token.json", 'r'))["TOKEN"]["APP_ID"]
    app_key = json.load(open("Edamam_token.json", 'r'))["TOKEN"]["APP_KEY"]

    toggle_recipes(True)
    url = f"https://api.edamam.com/search"

    if query.strip() == "":
        message_label.config(text="Please enter an ingredient!", fg='red')
        message_label.grid(row=6, column=0, pady=5)
        message_label.after(2000, lambda: message_label.grid_remove())
        toggle_recipes(False)
    else:
        if nums == 0:
            nums = 5
        message_label.config(text="Fetching recipe...", fg='green')
        message_label.grid(row=6, column=0, pady=5)
        message_label.update_idletasks()
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "q": query,
            "to": nums
        }

        response = requests.get(url, params=params)
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            if data['hits']:
                message_label.grid_remove()
                listbox.config(state='normal')
                listbox.delete('1.0', tk.END)
                listbox.insert(tk.END, f"Displaying recipes for {query}\n\n", "custom_font")
                for index, recipe in enumerate(data["hits"], start=1):
                    recipe = recipe['recipe']
                    ingredients = recipe['ingredientLines']
                    listed = '\n'.join([f'{index}) {value}' for index, value in enumerate(ingredients, start=1)])
                    listbox.insert(tk.END,
                                   f"{index}) Recipe name: {recipe['label']}\nURL: {recipe['url']}\nCalories: {recipe['calories']:.2f}"
                                   f"\nIngredients: \n{listed}\n\n", "custom_font")
                    print(f"{index}) {recipe['url']}")
                toggle_recipes(False)
                listbox.after(2000, listbox.grid(row=4, column=0, pady=5))
            else:
                message_label.config(text=f"Recipe not found for {query}!", fg='red')
                message_label.grid(row=6, column=0, pady=5)
                message_label.after(2000, lambda: message_label.grid_remove())
        else:
            message_label.config(text=f"Error fetching data. Status Code: {response.status_code}", fg='red')
            message_label.grid(row=6, column=0, pady=5)
            message_label.after(2000, lambda: message_label.grid_remove())
            toggle_recipes(False)
            print(f"Error fetching data. Status Code: {response.status_code}")


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
    style.set_theme('plastik')
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

    recipe_frame = tk.Frame(content_frame)
    message_label = tk.Label(recipe_frame, text="", font=("Quicksand", 17, "italic"))
    recipe_title = tk.Label(recipe_frame, text="Enter an ingredient / query: ", font=("Quicksand", 20, "italic"))
    recipe_entry = tk.Entry(recipe_frame, font=("Quicksand", 17, "italic"))
    recipe_nums = tk.IntVar()
    recipe_nums_label = tk.Label(recipe_frame, text="Enter number of recipes: ", font=("Quicksand", 20, "italic"))
    recipe_number = ttk.Spinbox(
        recipe_frame,
        from_=0,
        to=9999999999999,
        textvariable=recipe_nums,
        increment=1,
        font=("Quicksand", 15)

    )
    recipe_box = scrolledtext.ScrolledText(recipe_frame, wrap=tk.WORD, width=100, height=50)
    recipe_button = tk.Button(recipe_frame, text="Fetch", font=("Quicksand", 15, "bold"),
                              command=lambda: dishes(recipe_entry.get(), int(recipe_number.get()),
                                                     message_label,
                                                     recipe_box, toggle_recipe))

    def toggle_recipe(enable):
        if enable:
            recipe_box.delete("1.0", tk.END)
            recipe_title.grid(row=0, column=0, pady=10)
            recipe_entry.grid(row=1, column=0, pady=5)
            recipe_nums_label.grid(row=2, column=0, pady=10)
            recipe_number.grid(row=3, column=0, pady=5)
            recipe_button.grid(row=5, column=0, pady=15, columnspan=2)
            message_label.grid(row=6, column=0, pady=5)
            recipe_box.config(state='normal')
            recipe_box.tag_configure("custom_font", font=("Quicksand", 18), foreground="black")
            recipe_frame.pack()
        else:

            recipe_box.config(state='disabled')

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
        recipe_entry: recipe_number,
        recipe_number: recipe_button
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
