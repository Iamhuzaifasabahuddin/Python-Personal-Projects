import datetime
import json
import requests

api_key = json.load(open("Weather_token.json", 'r'))["TOKEN"]
url = "http://api.openweathermap.org/data/2.5/weather?"

params = {
    "q": "t",
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
        "appid": api_key,
        # "cnt": 5 * 8  # Fetch forecast for the next 3 days (24 hours * 3)
    }

    daily_forecast = []
    forecast_response = requests.get(forecast_url, params=params)
    results = forecast_response.json()

    # Skip the first entry as it corresponds to the current day
    for data in results['list'][1::8]:  # Use [1::8] to select every 8th entry starting from the second entry
        daily_forecast.append(
            {
                "day": datetime.datetime.fromtimestamp(data['dt']).strftime("%A"),
                "min_temp": f"{data['main']['temp_min'] - 273.15:.2f}°C",
                "max_temp": f"{data['main']['temp_max'] - 273.15:.2f}°C",
                "description": data["weather"][0]['description']
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
