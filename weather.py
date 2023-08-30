import requests

api_key = "78d640476dee416ef3231ec99561e834"
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

    print(f"Weather: {weather}")
    print(f"Temperature: {temperature} K")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
