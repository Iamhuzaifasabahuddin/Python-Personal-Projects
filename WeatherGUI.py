import datetime
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from PIL import Image, ImageTk
import io
import requests
from ttkthemes.themed_style import ThemedStyle


def show_message(message_label, text, colour, duration=2000):
    message_label.config(text=text, fg=colour)
    message_label.pack()
    message_label.after(duration, lambda: message_label.pack_forget())


def convert(temperature):
    celsius = temperature - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    return celsius, fahrenheit


def centered(window, width, height):
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    screen_centered_width, screen_centered_height = (screen_width - width) // 2, (screen_height - height) // 2
    return window.geometry(f"{width}x{height}+{screen_centered_width}+{screen_centered_height}")


def weather(location, listbox: tk.scrolledtext.ScrolledText, message_label, weather_toggle):
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    params = {
        "q": location.capitalize(),
        "appid": api_key
    }

    response = requests.get(weather_url, params=params)
    results = response.json()

    if location.strip() == "":
        show_message(message_label, text="Please Enter a City!", colour="red")
    else:
        if results["cod"] == "404":
            show_message(message_label, text="City Not Found!", colour="red")
            weather_toggle(False)
        else:
            show_message(message_label, text="Getting Weather....", colour="green")
            weather_desc = results["weather"][0]["description"]
            temperature = results["main"]["temp"]
            humidity = results["main"].get("humidity")
            feels_like = results["main"]["feels_like"]
            feels_like_celsius, feels_like_fahrenheit = convert(feels_like)
            celsius, fahrenheit = convert(temperature)
            icon_code = results["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            response_icon = requests.get(icon_url, stream=True)
            if response_icon.status_code == 200:  # code for API Success
                icon_data = response_icon.content
                icon_image = Image.open(io.BytesIO(icon_data))
                icon_image = icon_image.resize((70, 70))  # Adjust the size of the icon as needed
                icon_photo = ImageTk.PhotoImage(icon_image)

                listbox.insert(tk.END, f"City: {location.capitalize()}\n\n", "custom_font")

                # Store the icon_photo as an attribute of the listbox widget
                listbox.icon_photo = icon_photo

                listbox.image_create(tk.END, image=icon_photo)
                listbox.insert(tk.END, f"\nWeather: {weather_desc}\nTemperature: {celsius:.2f}°C, {fahrenheit:.2f}°F\n"
                                       f"Feels like {feels_like_celsius:.2f}°C, {feels_like_fahrenheit:.2f}°F\n"
                                       f"Humidity {humidity}%\n", "custom_font")
                listbox.after(2000, lambda: listbox.pack(pady=10))
                weather_toggle(False)
            else:
                print("Icon not found")


def forecast(location, days, message_label, forecast_listbox: tk.scrolledtext.ScrolledText, forecast_toggle):
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    if location.strip() == "":
        show_message(message_label, text="Enter a City!", colour="red")
        return

    if not days or not days.isdigit() or days < 0:
        show_message(message_label, text="Invalid input. Defaulting to 5 days.", colour="red")
    else:
        days = min(int(days), 5)  # Limit days to a maximum of 5

        weather_params = {
            "q": location.capitalize(),
            "appid": api_key
        }
        response_weather = requests.get(weather_url, params=weather_params).json()
        if response_weather['cod'] == '404':
            show_message(message_label, text="City Not Found!", colour="red")
            forecast_toggle(False)
        else:
            lat, lon = response_weather['coord']['lat'], response_weather['coord']['lon']

            params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "cnt": days * 8  # 3 hours interval for the api for each day
            }

            daily_forecast = []
            forecast_response = requests.get(forecast_url, params=params)
            results = forecast_response.json()
            for data in results['list'][1::8]:  # Use ::8 due to 3 hours timespan, get the 8th value excluding today
                day_timestamp = data['dt']
                day = datetime.datetime.fromtimestamp(day_timestamp).strftime("%A")
                converted_c_min, converted_f_min = convert(data['main']['temp_min'])
                converted_c_max, converted_f_max = convert(data['main']['temp_max'])
                daily_forecast.append(
                    {
                        "day": day,
                        "min_temp": f"{converted_c_min:.2f}°C/ {converted_f_min:.2f}°F",
                        "max_temp": f"{converted_c_max:.2f}°C/ {converted_f_max:.2f}°F",
                        "description": data["weather"][0]['description']
                    }
                )

            show_message(message_label, text=f"Getting Forecast for {days} Days...", colour="green")
            forecast_listbox.insert(tk.END, f"Forecast For The Next {days} Days For {location.capitalize()}:\n\n",
                                    "custom_font")
            for values in daily_forecast:
                forecast_listbox.insert(tk.END, f"Day: {values['day']}\nMinimum Temperature: {values['min_temp']}\n"
                                                f"Maximum Temperature: {values['max_temp']}\nWeather: {values['description']}\n\n",
                                        "custom_font")
            forecast_listbox.after(2000, lambda: forecast_listbox.pack(pady=10))
            forecast_toggle(False)


def gui():
    window = tk.Tk()
    window.title("Weather App")
    style = ThemedStyle(window)
    style.set_theme("breeze")
    centered(window, 500, 500)

    # Create a frame for main fields
    frame_main = tk.Frame(window)
    frame_main.pack(pady=20)

    # Weather fields
    Weather_label = tk.Label(frame_main, text="Enter a city:", font=("Quicksand", 25, "italic"))
    Weather_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    Weather_button = tk.Button(frame_main, text="ADD", command=lambda: weather(Weather_entry.get(),
                                                                               Weather_box,
                                                                               Weather_message_label, weather_toggle)
                               , font=("Merriweather", 15))

    Weather_message_label = tk.Label(frame_main, text="", font=("Quicksand", 15, "italic"))
    Weather_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=80, height=40, background="#E1E7DE",
                                            borderwidth=4)

    # Forecast fields
    forecast_label = tk.Label(frame_main, text="Enter a city: ", font=("Quicksand", 25, "italic"), anchor="w")
    forecast_message_label = tk.Label(frame_main, text="", font=("Quicksand", 15, "italic"))
    forecast_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    forecast_Days_label = tk.Label(frame_main, text="Enter number of days: ",
                                   font=("Quicksand", 25, "italic"), anchor="w")
    forecast_days_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    forecast_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=80, height=40, background="#E1E7DE",
                                             borderwidth=4, )
    forecast_button = tk.Button(frame_main, text="Forecast", command=lambda:
    forecast(forecast_entry.get(), forecast_days_entry.get(), forecast_message_label, forecast_box, forecast_toggle),
                                font=("Merriweather", 15))

    Options = ["", "Weather", "Forecast", "Weather & Forecast"]
    Options_label = tk.Label(frame_main, text="Select a Task: ", font=("Quicksand", 25, "italic"))
    option = tk.StringVar()
    Option_box = tk.ttk.Combobox(frame_main, textvariable=option, font=("Merriweather", 15))
    Option_box['values'] = Options
    Option_box['state'] = "readonly"
    Options_label.pack(pady=10)

    def weather_toggle(enable):
        if enable:
            Weather_label.pack(pady=5)
            Weather_entry.pack(pady=10)
            Weather_button.pack(pady=10)
            Weather_box.delete("1.0", tk.END)
            Weather_box.config(state="normal")
            Weather_box.tag_configure("custom_font", font=("Quicksand", 20), foreground="black")
        else:
            Weather_button.pack_forget()
            Weather_label.pack_forget()
            Weather_entry.pack_forget()
            Weather_box.config(state="disabled")
            Weather_entry.delete(0, tk.END)

    def forecast_toggle(enable):
        if enable:
            forecast_label.pack(pady=5)
            forecast_entry.pack(pady=10)
            forecast_Days_label.pack(pady=5)
            forecast_days_entry.pack(pady=10)
            forecast_button.pack(pady=10)
            forecast_box.delete("1.0", tk.END)
            forecast_box.config(state="normal")
            forecast_box.config(state="normal")
            forecast_box.tag_configure("custom_font", font=("Quicksand", 18), foreground="black")
        else:
            forecast_entry.pack_forget()
            forecast_label.pack_forget()
            forecast_days_entry.pack_forget()
            forecast_Days_label.pack_forget()
            forecast_button.pack_forget()
            forecast_box.config(state="disabled")
            forecast_entry.delete(0, tk.END)
            forecast_days_entry.delete(0, tk.END)

    def get_value(event):
        selected = option.get()
        if selected == "Weather":
            weather_toggle(True)
            forecast_toggle(False)
            Weather_box.pack_forget()
            forecast_box.pack_forget()
        elif selected == "Forecast":
            forecast_toggle(True)
            weather_toggle(False)
            forecast_box.pack_forget()
            Weather_box.pack_forget()

    entry_mapping = {
        Weather_entry: Weather_button,
        forecast_entry: forecast_days_entry,
        forecast_days_entry: forecast_button
    }

    def widget_handler(event):
        focused_widget = window.focus_get()
        for widget, next_widget in entry_mapping.items():
            if widget == focused_widget:
                next_widget.focus()
                break
        for buttons in [Weather_button, forecast_button]:
            if focused_widget == buttons:
                buttons.invoke()
        # forecast_button.focus_set()

    for widget in entry_mapping:
        widget.bind("<Return>", widget_handler)
    for button in [Weather_button, forecast_button]:
        button.bind("<Return>", widget_handler)

    def close():
        if messagebox.askyesno(title="Exit", message="Do You Wanna Exit ?"):
            window.destroy()
            messagebox.showinfo(title="Exited Application", message="Exited Successfully")

    window.protocol("WM_DELETE_WINDOW", close)

    Option_box.bind("<<ComboboxSelected>>", get_value)
    Option_box.pack(pady=10)

    window.mainloop()


if __name__ == '__main__':
    gui()
