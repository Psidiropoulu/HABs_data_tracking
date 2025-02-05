import requests
from datetime import datetime
from models import WeatherData
from .config import API_KEY, BASE_URL, LOCATION

def fetch_and_store_weather_data():
    params = {
        'q': LOCATION,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        WeatherData.objects.create(
            description=data['weather'][0]['description'],
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data['wind']['speed'],
            wind_direction=data['wind']['deg'],
            visibility=data['visibility'],
            cloud_coverage=data['clouds']['all'],
            sunrise=datetime.fromtimestamp(data['sys']['sunrise']),
            sunset=datetime.fromtimestamp(data['sys']['sunset'])
        )
        print("Weather data stored successfully.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Error: {response.text}")
