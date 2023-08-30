import json
import tkinter as tk
from tkinter import scrolledtext

import requests


def convert(temperature):
    celsius = temperature - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    return celsius, fahrenheit


def weather(location, listbox: tk.scrolledtext.ScrolledText, main_entry, messsage_label):
    api_key = json.load(open("Weather_toke.json", 'r'))["TOKEN"]
    url = "http://api.openweathermap.org/data/2.5/weather?"

    params = {
        "q": location,
        "appid": api_key
    }

    response = requests.get(url, params=params)
    results = response.json()

    if location.strip() == "":
        messsage_label.config(text="Please enter a city", fg="red")
        messsage_label.pack()
        messsage_label.after(2000, lambda: messsage_label.pack_forget())
    else:
        if results["cod"] == "404":
            print("City not found")
        else:
            weather_desc = results["weather"][0]["description"]
            temperature = results["main"]["temp"]
            celsius, fahrenheit = convert(temperature)
            main_entry.delete(0, tk.END)
            listbox.insert(tk.END, f"City: {location.capitalize()}\n\n")
            listbox.insert(tk.END, f"Weather: {weather_desc}\nTemperature: {celsius:.2f}°C, {fahrenheit:.2f}°F\n\n")
            listbox.pack()


def gui():
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Weather App")

    # Create a frame for main fields
    frame_main = tk.Frame(window)
    frame_main.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Center the main frame
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Main fields
    main_label = tk.Label(frame_main, text="Enter a city:", font=("Quicksand", 25, "italic"))
    main_label.pack(pady=10)

    main_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    main_entry.pack(pady=10)

    main_button = tk.Button(frame_main, text="ADD", command=lambda: weather(main_entry.get(),
                                                                            main_box, main_entry, main_message_label))
    main_button.pack(pady=15)

    main_message_label = tk.Label(frame_main, text="", font=("Quicksand", 25, "italic"))

    main_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=40, height=10)

    entry_mapping = {
        main_entry: main_button
    }

    def widget_handler(event):
        focused_widget = window.focus_get()
        for widget, next_widget in entry_mapping.items():
            if widget == focused_widget:
                next_widget.focus()
                break
        for buttons in [main_button]:
            if focused_widget == buttons:
                buttons.invoke()

    for widget in entry_mapping:
        widget.bind("<Return>", widget_handler)
    for button in [main_button]:
        button.bind("<Return>", widget_handler)

    window.mainloop()


if __name__ == '__main__':
    gui()
