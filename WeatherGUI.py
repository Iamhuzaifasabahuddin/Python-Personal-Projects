import datetime
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

import requests
from ttkthemes.themed_style import ThemedStyle


def convert(temperature):
    celsius = temperature - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    return celsius, fahrenheit


def centered(window, width, height):
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()  # Corrected this line
    screen_centered_width, screen_centered_height = (screen_width - width) // 2, (screen_height - height) // 2
    return window.geometry(f"{width}x{height}+{screen_centered_width}+{screen_centered_height}")


def weather(location, listbox: tk.scrolledtext.ScrolledText, main_entry, message_label):
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    params = {
        "q": location,
        "appid": api_key
    }

    response = requests.get(weather_url, params=params)
    results = response.json()

    if location.strip() == "":
        message_label.config(text="Please enter a city", fg="red")
        message_label.pack()
        message_label.after(2000, lambda: message_label.pack_forget())
    else:
        if results["cod"] == "404":
            print("City not found")
        else:
            weather_desc = results["weather"][0]["description"]
            temperature = results["main"]["temp"]
            humidity = results["main"].get("humidity")
            feels_like = results["main"]["feels_like"]
            feels_like_celsius, feels_like_fahrenheit = convert(feels_like)
            celsius, fahrenheit = convert(temperature)
            listbox.config(state="normal")
            main_entry.delete(0, tk.END)
            listbox.insert(tk.END, f"City: {location.capitalize()}\n\n")
            listbox.insert(tk.END, f"Weather: {weather_desc}\nTemperature: {celsius:.2f}°C, {fahrenheit:.2f}°F\n"
                                   f"Feels like {feels_like_celsius:.2f}°C, {feels_like_fahrenheit:.2f}°F"
                                   f"Humidty {humidity}%\n")
            listbox.config(state="disabled")
            listbox.pack()


def forecast(location, message_label, forecast_listbox: tk.scrolledtext.ScrolledText):
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    weather_params = {
        "q": location,
        "appid": api_key
    }
    response_weather = requests.get(weather_url, params=weather_params).json()
    lat, lon = response_weather['coord']['lat'], response_weather['coord']['lon']

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }

    daily_forecast = []
    forecast_response = requests.get(forecast_url, params=params)
    results = forecast_response.json()
    for data in results['list'][:5]:  # Use 'list' instead of 'daily'
        day_timestamp = data['dt']
        day = datetime.datetime.fromtimestamp(day_timestamp).strftime("%A")
        daily_forecast.append(
            {
                "day": day,
                "min_temp": f"{data['main']['temp_min'] - 273.15:.2f}degree",
                "max_temp": f"{data['main']['temp_max'] - 273.15:.2f}",
                "description": data["weather"][0]['description']
            }
        )

    forecast_listbox.config(state="normal")
    forecast_listbox.delete("1.0", tk.END)
    forecast_listbox.insert(tk.END, f"Forecast For The Next 5 Days For {location}:\n\n")
    for values in daily_forecast:
        forecast_listbox.insert(tk.END, f"Day: {values['day']}\n Minimum Temperature: {values['min_temp']}\n"
                                        f"Maximum Temperature: {values['max_temp']}\n Weather: {values['description']}\n\n")
    forecast_listbox.config(state="disabled")
    forecast_listbox.pack()


def gui():
    window = tk.Tk()
    window.title("Weather App")
    style = ThemedStyle(window)
    style.set_theme("breeze")
    centered(window, 500, 500)

    # Create a frame for main fields
    frame_main = tk.Frame(window)
    frame_main.pack()

    # Main fields
    main_label = tk.Label(frame_main, text="Enter a city:", font=("Quicksand", 25, "italic"))

    main_entry = tk.Entry(frame_main, font=("Quicksand", 15))

    main_button = tk.Button(frame_main, text="ADD", command=lambda: weather(main_entry.get(),
                                                                            main_box, main_entry, main_message_label)
                            , font=("Merriweather", 15))
    forecast_button = tk.Button(frame_main, text="Forecast", command=lambda:
    forecast(main_entry.get(), main_message_label, forecast_box), font=("Merriweather", 15))


    main_message_label = tk.Label(frame_main, text="", font=("Quicksand", 25, "italic"))

    main_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=40, height=10)
    forecast_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=40, height=10)

    main_label.pack(pady=10)
    main_entry.pack(pady=10)
    main_button.pack(pady=15)
    forecast_button.pack(pady=15)

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
        forecast_button.focus_set()

    for widget in entry_mapping:
        widget.bind("<Return>", widget_handler)
    for button in [main_button, forecast_button]:
        button.bind("<Return>", widget_handler)

    def close():
        if messagebox.askyesno(title="Exit", message="Do You Wanna Exit ?"):
            window.destroy()
            messagebox.showinfo(title="Exited Application", message="Exited Successfully")

    window.protocol("WM_DELETE_WINDOW", close)

    window.mainloop()


if __name__ == '__main__':
    gui()
