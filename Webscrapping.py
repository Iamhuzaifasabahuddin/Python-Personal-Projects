import pprint

import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

Url = "https://weather.com/en-GB/weather/today/l/c80be98888b56ecfaea450054dbd63fa31331a899214910e83725cf7ee70eaf5"
response = requests.get(Url)

if response.status_code == HTTPStatus.OK:
    soup = BeautifulSoup(response.content, "html.parser")

    temperature_element = soup.find('span', class_='TodayDetailsCard--feelsLikeTempValue--2icPt')
    print(f"current temperature: {temperature_element.text}")
    temperature_element = soup.find('div', class_='WeatherDetailsListItem--wxData--kK35q')

    if temperature_element:
        temperature_spans = temperature_element.find_all('span', {'data-testid': 'TemperatureValue'})

        if len(temperature_spans) == 2:
            first_temperature = temperature_spans[0].text.strip()
            second_temperature = temperature_spans[1].text.strip()

            print(f"Temperature 1: {first_temperature}")
            print(f"Temperature 2: {second_temperature}")
        else:
            print("Temperature spans not found or not in the expected format.")
    else:
        print("Temperature element not found on the page.")
else:
    print(f"Request failed: {response.status_code}!"
          )
