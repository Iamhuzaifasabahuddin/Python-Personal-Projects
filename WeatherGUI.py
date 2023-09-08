import datetime
import json
import logging
import statistics
import tkinter as tk
import tkinter.scrolledtext
from tkinter import scrolledtext, messagebox, ttk
from typing import Callable

from PIL import Image, ImageTk
import io
import requests
from ttkthemes.themed_style import ThemedStyle


def show_message(message_label, text, colour, duration=2000):
    """
    Display a message on a label widget with specified text and color, and then hide it after a specified duration.

    Args:
        message_label (tk.Label): The label widget to display the message.
        text (str): The text message to display.
        colour (str): The color (foreground) of the text.
        duration (int, optional): The duration in milliseconds for which the message should be displayed. Default is 2000ms (2 seconds).
    """
    message_label.config(text=text, fg=colour)
    message_label.pack()
    message_label.after(duration, lambda: message_label.pack_forget())


def convert(temperature):
    """
    Convert a temperature from Kelvin to Celsius and Fahrenheit.

    Args:
        temperature (float): The temperature in Kelvin.

    Returns:
        tuple: A tuple containing two floats representing the temperature in Celsius and Fahrenheit, respectively.
    """
    celsius = temperature - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    logging.info("Conversion!")
    return celsius, fahrenheit


def centered(window, width, height):
    """
    Center a tkinter window on the screen.

    Args:
        window (tk.Tk): The tkinter window to center.
        width (int): The width of the window.
        height (int): The height of the window.

    Returns:
        None
    """
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    screen_centered_width, screen_centered_height = (screen_width - width) // 2, (screen_height - height) // 2
    logging.info("Centralized Window!")
    return window.geometry(f"{width}x{height}+{screen_centered_width}+{screen_centered_height}")


def weather(location, listbox: tk.scrolledtext.ScrolledText, message_label, weather_toggle):
    """
    Retrieve and display weather information for a given location.

    Args:
        location (str): The name of the city for which weather information is requested.
        listbox (tk.scrolledtext.ScrolledText): The widget to display the weather information.
        message_label (tk.Label): The label widget for displaying messages.
        weather_toggle (function): A function to toggle the weather interface.

    Returns:
        None
    """
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
            logging.info("City Not Found!")
            weather_toggle(False)
        else:
            show_message(message_label, text="Getting Weather....", colour="green")
            logging.info("Getting Weather From The API!")
            weather_desc = results["weather"][0].get("description", "N/A")
            temperature = results["main"].get("temp", "N/A")
            humidity = results["main"].get("humidity", "N/A")
            feels_like = results["main"].get("feels_like", "N/A")
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
                logging.info("Weather From The API Displayed!")
                weather_toggle(False)
            else:
                logging.info("Icon From The API Doesnt Exist!")
                print("Icon not found")


def forecast(location, days, message_label, forecast_listbox: tk.scrolledtext.ScrolledText, forecast_toggle):
    """
    Retrieve and display weather forecast information for a given location.

    Args:
        location (str): The name of the city for which the weather forecast is requested.
        days (str): The number of days for the forecast.
        message_label (tk.Label): The label widget for displaying messages.
        forecast_listbox (tk.scrolledtext.ScrolledText): The widget to display the forecast information.
        forecast_toggle (function): A function to toggle the forecast interface.

    Returns:
        None
    """
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    if location.strip() == "":
        show_message(message_label, text="Enter a City!", colour="red")
        logging.info("Invalid Input!")
        return

    if not days or not days.isdigit() or int(days) < 0:
        show_message(message_label, text="Invalid input. Defaulting to 5 days.", colour="red")
        logging.info("Invalid Input!")
    else:
        days = min(int(days), 5)  # Limit days to a maximum of 5

        weather_params = {
            "q": location.capitalize(),
            "appid": api_key
        }
        response_weather = requests.get(weather_url, params=weather_params).json()
        if response_weather['cod'] == '404':
            show_message(message_label, text="City Not Found!", colour="red")
            logging.info("City Not Found!")
            forecast_toggle(False)
        else:
            lat, lon = response_weather['coord']['lat'], response_weather['coord']['lon']

            params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "cnt": days * 8  # 3 hours interval for the api for each day
            }

            daily_forecast = {}
            forecast_response = requests.get(forecast_url, params=params)
            results = forecast_response.json()
            for data in results['list'][1::]:
                day_timestamp = data['dt']
                day = datetime.datetime.fromtimestamp(day_timestamp).strftime("%A")
                converted_c_min, converted_f_min = convert(data['main']['temp_min'])
                converted_c_max, converted_f_max = convert(data['main']['temp_max'])

                if day not in daily_forecast:
                    daily_forecast[day] = {
                        "min_temps": [],
                        "max_temps": [],
                        "descriptions": []
                    }

                daily_forecast[day]["min_temps"].append(converted_c_min)
                daily_forecast[day]["max_temps"].append(converted_c_max)
                daily_forecast[day]["descriptions"].append(data["weather"][0]['description'])

            show_message(message_label, text=f"Getting Forecast for {days} Days...", colour="green")
            logging.info("Getting Forecast From The API!")
            forecast_listbox.insert(tk.END, f"Forecast For The Next {days} Days For {location.capitalize()}:\n\n",
                                    "custom_font")

            for day, data in daily_forecast.items():
                avg_min_temp = sum(data["min_temps"]) / len(data["min_temps"])
                avg_max_temp = sum(data["max_temps"]) / len(data["max_temps"])
                avg_description = statistics.mode(data["descriptions"])

                forecast_listbox.insert(tk.END, f"Day: {day}\nAverage Minimum Temperature: {avg_min_temp:.2f}°C\n"
                                                f"Average Maximum Temperature: {avg_max_temp:.2f}°C\n"
                                                f"Mode Weather: {avg_description}\n\n", "custom_font")

            forecast_listbox.after(2000, lambda: forecast_listbox.pack(pady=10))
            logging.info("Forecast From The API Displayed Successfully!")
            forecast_toggle(False)


def weather_and_forecast(location: str, days: int, wflistbox: tkinter.scrolledtext.ScrolledText,
                         message_label: tk.Label, toggle_wf: Callable):
    """
    Get weather and forecast information for a specified location and display it in a scrolled text box.

    Args:
        location (str): The name of the city for which weather and forecast information is requested.
        days (int): The number of days to forecast.
        wflistbox (tkinter.scrolledtext.ScrolledText): The scrolled text box widget to display the information.
        message_label (tk.Label): The label widget to display messages or errors.
        toggle_wf (Callable): A function used to toggle the display of the weather and forecast information.

    Returns:
        None
    """
    api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    if location.strip() == "":
        show_message(message_label, text="Enter a City!", colour="red")
        logging.info("Invalid Input!")
        return

    if not days or not days.isdigit() or int(days) < 0:
        show_message(message_label, text="Invalid input. Defaulting to 5 days.", colour="red")
        logging.info("Invalid Input!")
    else:
        days = min(int(days), 5)  # Limit days to a maximum of 5
        weather_params = {
            "q": location.capitalize(),
            "appid": api_key
        }

        weather_response = requests.get(weather_url, params=weather_params).json()
        if weather_response['cod'] == "404":
            show_message(message_label, text="City Not Found!", colour="red")
            logging.info("City Not Found!")
        else:
            lat, lon = weather_response['coord']['lat'], weather_response['coord']['lon']

            forecast_params = {
                "appid": api_key,
                "cnt": int(days) * 8,
                "lat": lat,
                "lon": lon
            }

            forecast_response = requests.get(forecast_url, params=forecast_params).json()

            show_message(message_label, text="Getting Weather & Forecast....", colour="green")
            logging.info("Getting Weather & Forecast From The API!")
            weather_desc = weather_response["weather"][0].get("description", "N/A")
            temperature = weather_response["main"].get("temp", "N/A")
            humidity = weather_response["main"].get("humidity", "N/A")
            feels_like = weather_response["main"].get("feels_like", "N/A")
            feels_like_celsius, feels_like_fahrenheit = convert(feels_like)
            celsius, fahrenheit = convert(temperature)

            forecasted_Data = {}
            for data in forecast_response['list']:
                day_timestamp = data['dt']
                day = datetime.datetime.fromtimestamp(day_timestamp).strftime("%A")
                converted_c_min, converted_f_min = convert(data['main']['temp_min'])
                converted_c_max, converted_f_max = convert(data['main']['temp_max'])

                if day not in forecasted_Data:
                    forecasted_Data[day] = {
                        "min_temps": [],
                        "max_temps": [],
                        "descriptions": []
                    }

                forecasted_Data[day]["min_temps"].append(converted_c_min)
                forecasted_Data[day]["max_temps"].append(converted_c_max)
                forecasted_Data[day]["descriptions"].append(data["weather"][0]['description'])

            wflistbox.insert(tk.END, f"Weather & Forecast for {location.capitalize()}\n\n", "custom_font")
            logging.info("Getting Weather & Forecast From The API!")
            wflistbox.insert(tk.END,
                             f"Weather details:\nWeather: {weather_desc}\nTemperature: {celsius:.2f}°C, {fahrenheit:.2f}°F\n"
                             f"Feels like {feels_like_celsius:.2f}°C, {feels_like_fahrenheit:.2f}°F\n"
                             f"Humidity {humidity}%\n\n", "custom_font")

            for day, data in forecasted_Data.items():
                avg_min_temp = sum(data["min_temps"]) / len(data["min_temps"])
                avg_max_temp = sum(data["max_temps"]) / len(data["max_temps"])
                avg_description = statistics.mode(data["descriptions"])

                wflistbox.insert(tk.END,
                                 f"Forecast details:\nDay: {day}\nAverage Minimum Temperature: {avg_min_temp:.2f}°C\n"
                                 f"Average Maximum Temperature: {avg_max_temp:.2f}°C\n"
                                 f"Mode Weather: {avg_description}\n\n",
                                 "custom_font")

            wflistbox.after(2000, lambda: wflistbox.pack())
            logging.info("Weather & Forecast From The API Displayed Successfully!")
        toggle_wf(False)


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
                               , font=("Quicksand", 15))

    Weather_message_label = tk.Label(frame_main, text="", font=("Quicksand", 15, "italic"))
    Weather_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=80, height=40, background="#E1E7DE",
                                            borderwidth=4)

    # Forecast fields
    forecast_label = tk.Label(frame_main, text="Enter a city: ", font=("Quicksand", 25, "italic"))
    forecast_message_label = tk.Label(frame_main, text="", font=("Quicksand", 15, "italic"))
    forecast_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    forecast_Days_label = tk.Label(frame_main, text="Enter number of days: ",
                                   font=("Quicksand", 25, "italic"), anchor="w")
    forecast_days_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    forecast_box = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=80, height=40, background="#E1E7DE",
                                             borderwidth=4, )
    forecast_button = tk.Button(frame_main, text="Forecast", command=lambda:
    forecast(forecast_entry.get(), forecast_days_entry.get(), forecast_message_label, forecast_box, forecast_toggle),
                                font=("Quicksand", 15))

    weather_and_forecast_label = tk.Label(frame_main, text="Enter a city: ", font=("Quicksand", 25, "italic"))
    weather_and_forecast_entry = tk.Entry(frame_main, font=("Quicksand", 15))
    weather_and_forecast_label_2 = tk.Label(frame_main, text="Enter number of days: ", font=("Quicksand", 25, "italic"))
    weather_and_forecast_days = tk.Entry(frame_main, font=("Quicksand", 15))
    weather_and_forecast_message = tk.Label(frame_main, text="", font=("Quicksand", 15, "italic"))
    weather_and_forecast_box = tk.scrolledtext.ScrolledText(frame_main, wrap=tk.WORD, width=80, height=40,
                                                            background="#E1E7DE",
                                                            borderwidth=4)
    weather_and_forecast_button = tk.Button(frame_main, text="Get", command=lambda:
    weather_and_forecast(weather_and_forecast_entry.get(), weather_and_forecast_days.get(), weather_and_forecast_box,
                         weather_and_forecast_message,
                         weather_and_forecast_toggle)
                                            , font=("Quicksand", 15))

    Options = ["", "Weather", "Forecast", "Weather & Forecast"]
    Options_label = tk.Label(frame_main, text="Select a Task: ", font=("Quicksand", 25, "italic"))
    option = tk.StringVar()
    Option_box = tk.ttk.Combobox(frame_main, textvariable=option, font=("Quicksand", 15))
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

    def weather_and_forecast_toggle(enable):
        if enable:
            weather_and_forecast_label.pack(pady=5)
            weather_and_forecast_entry.pack(pady=10)
            weather_and_forecast_label_2.pack(pady=5)
            weather_and_forecast_days.pack(pady=10)
            weather_and_forecast_button.pack(pady=10)
            weather_and_forecast_box.config(state="normal")
            weather_and_forecast_box.delete("1.0", tk.END)
            weather_and_forecast_box.tag_configure("custom_font", font=("Quicksand", 18), foreground="black")
        else:
            weather_and_forecast_label.pack_forget()
            weather_and_forecast_entry.pack_forget()
            weather_and_forecast_label_2.pack_forget()
            weather_and_forecast_days.pack_forget()
            weather_and_forecast_button.pack_forget()
            weather_and_forecast_entry.delete(0, tk.END)
            weather_and_forecast_days.delete(0, tk.END)
            weather_and_forecast_box.config(state="disabled")

    def get_value(event):
        selected = option.get()
        if selected == "Weather":
            weather_toggle(True)
            forecast_toggle(False)
            Weather_box.pack_forget()
            forecast_box.pack_forget()
            weather_and_forecast_box.pack_forget()
        elif selected == "Forecast":
            forecast_toggle(True)
            weather_toggle(False)
            forecast_box.pack_forget()
            Weather_box.pack_forget()
            weather_and_forecast_box.pack_forget()
        elif selected == "Weather & Forecast":
            weather_and_forecast_toggle(True)
            forecast_toggle(False)
            weather_toggle(False)
            forecast_box.pack_forget()
            Weather_box.pack_forget()
            weather_and_forecast_box.pack_forget()

    entry_mapping = {
        Weather_entry: Weather_button,
        forecast_entry: forecast_days_entry,
        forecast_days_entry: forecast_button,
        weather_and_forecast_entry: weather_and_forecast_days,
        weather_and_forecast_days: weather_and_forecast_button
    }

    def widget_handler(event):
        focused_widget = window.focus_get()
        for widget, next_widget in entry_mapping.items():
            if widget == focused_widget:
                next_widget.focus()
                break
        for buttons in [Weather_button, forecast_button, weather_and_forecast_button]:
            if focused_widget == buttons:
                buttons.invoke()

    for widget in entry_mapping:
        widget.bind("<Return>", widget_handler)
    for button in [Weather_button, forecast_button, weather_and_forecast_button]:
        button.bind("<Return>", widget_handler)

    def close():
        if messagebox.askyesno(title="Exit", message="Do You Wanna Exit ?"):
            window.destroy()
            messagebox.showinfo(title="Exited Application", message="Exited Successfully")

    window.protocol("WM_DELETE_WINDOW", close)

    Option_box.bind("<<ComboboxSelected>>", get_value)
    Option_box.pack(pady=10)

    window.mainloop()


def logging_func():
    """Creates a console and file logging handler that logs messages"""
    logging.basicConfig(level=logging.INFO, format='%(funcName)s - %(message)s - %(asctime)s - %(levelname)s',
                        datefmt = "%Y-%m-%d %I:%M:%S %p")

    # Create a file handler
    file_handler = logging.FileHandler('Weather_App.log')
    file_handler.setLevel(logging.WARNING)  # Set the desired log level for the file handler

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(funcName)s - %(message)s - %(asctime)s - %(levelname)s',
                                  "%Y-%m-%d %I:%M:%S %p")
    file_handler.setFormatter(formatter)

    # Get the root logger and add the handlers
    logger = logging.getLogger('')
    logger.addHandler(file_handler)


if __name__ == '__main__':
    logging_func()
    gui()
