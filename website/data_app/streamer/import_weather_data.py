from django.core.management.base import BaseCommand
import requests
from data_app.models import WeatherData
from datetime import datetime

def import_data():
    # Replace with your logic to import data
    new_weather_data = WeatherData(
        temperature=25.0,  # Replace with actual data fields
        humidity=60.0,
        pressure=1013.0,
        timestamp = datetime.strptime('2024-11-10 13:00:00', '%Y-%m-%d %H:%M:%S'
    )
    new_weather_data.save()
    print("Weather data imported successfully.")

if __name__ == "__main__":
    import_data()
