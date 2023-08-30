import datetime
import json

import requests

api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
url = "http://api.openweathermap.org/data/2.5/weather?"

params = {
    "q": "Leicester",
    "appid": api_key
}

response = requests.get(url, params=params)
data = response.json()
print(data)
if data["cod"] == "404":
    print("City not found")
else:
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    feels = data["main"]["feels_like"]
    print(f"Weather: {weather}")
    print(f"Temperature: {temperature} K")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(feels)

import json
import datetime
import requests


def forecast(location):
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
    for data2 in results['list'][:5]:  # Use 'list' instead of 'daily'
        print(data2['dt'])
        daily_forecast.append(
            {
                "day": datetime.datetime.fromtimestamp(data2['dt']).strftime("%A"),
                "min_temp": f"{data2['main']['temp_min'] - 273.15:.2f}",  # Access min temp using main['temp_min']
                "max_temp": f"{data2['main']['temp_max'] - 273.15:.2f}",  # Access max temp using main['temp_max']
                "description": data2["weather"][0]['description']
            }
        )
    return daily_forecast


# Test the forecast function
if __name__ == "__main__":
    location = "New York"  # Replace with the desired location
    forecast_data = forecast(location)
    for data in forecast_data:
        print(f"Day: {data['day']}")
        print(f"Min Temp: {data['min_temp']}°C")
        print(f"Max Temp: {data['max_temp']}°C")
        print(f"Description: {data['description']}\n")
