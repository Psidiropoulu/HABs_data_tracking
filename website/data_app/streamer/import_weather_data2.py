# This is from an old project I wrote which displays live weather forecast data for a location

import sys
from geopy.geocoders import Nominatim
# from kgcpy import lookupCZ
import pandas as pd
from pymeteosource.api import Meteosource
from pymeteosource.types import sections, units
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import os
from tabulate import tabulate
import matplotlib.pyplot as plt


def weather_data():

    lat = 53.12
    lon = 1.23

    # current weather
    current_summary, current_icon, current_temp, current_precipitation, current_wind_speed, current_wind_direction, current_cloud_cover, df_hourly, df_daily = get_weather(lat, lon)
    print("ITS CURRENT WEATHER:")
    print(f"Summary: {current_summary}")
    print(f"Icon: {current_icon}")
    print(f"Temperature: {current_temp} °C")
    print(f"Precipitation: {current_precipitation} mm")
    print(f"Wind Speed: {current_wind_speed} m/s")
    print(f"Wind Direction: {current_wind_direction}")
    print(f"Cloud Cover: {current_cloud_cover}%\n")

    # hourly forecast
    print("48-HOUR WEATHER FORECAST:")
    visualize_hourly_forecast(df_hourly)
    print(f"\n")

    # daily forcast
    print(f"7-DAY WEATHER FORECAST:\n")
    visualize_daily_forecast(df_daily)


def get_weather(lat, lon):
    API_KEY = 's0ciwphgts0xgeu6nt3azyhhmwq7x0z2jb4bkik6'
    meteosource = Meteosource(API_KEY, 'free')

    forecast = meteosource.get_point_forecast(
        lat=lat,
        lon=lon,
        sections=[sections.CURRENT, sections.HOURLY, sections.DAILY_PARTS],
        units=units.METRIC
    )

    current_weather = forecast.current
    temp = current_weather['temperature']
    summary = current_weather['summary']
    icon = current_weather['icon']
    precipitation = current_weather['precipitation']['total']
    wind_speed = current_weather['wind']['speed']
    wind_direction = current_weather['wind']['dir']
    cloud_cover = current_weather['cloud_cover']

    df_hourly = forecast.hourly.to_pandas()
    df_daily = forecast.daily.to_pandas()


    return (summary, icon, temp, precipitation, wind_speed, wind_direction, cloud_cover, df_hourly, df_daily)


def visualize_hourly_forecast(df):

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8, 12), sharex=True)


    # Plot 1: Temperature
    axes[0].plot(df.index, df['temperature'], color='#8071A0', marker='o')
    axes[0].set_ylabel('Temperature (°C)')
    axes[0].set_title('Temperature')

    # Plot 2: Precipitation
    axes[1].plot(df.index, df['precipitation_total'], color='#27408B', marker='o')
    axes[1].set_ylabel('Precipitation (mm)')
    axes[1].set_title('Precipitation')

    # Plot 3: Cloud Cover
    axes[2].plot(df.index, df['cloud_cover_total'], color='#4A708B', marker='o')
    axes[2].set_ylabel('Cloud Cover (%)')
    axes[2].set_title('Cloud Cover')

    # Plot 4: Wind Speed
    axes[3].plot(df.index, df['wind_speed'], color='#556B2F', marker='o')
    axes[3].set_ylabel('Wind Speed (m/s)')
    axes[3].set_title('Wind Speed')

    for ax in axes[1:]:
        ax.set_xlim(df.index.min(), df.index.max())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    plt.tight_layout()
    plt.show()



def visualize_daily_forecast(df):
    table_data = []

    weather_icon = {
        1: "❓",   # Not available
        2: "☀️",  # Sunny
        3: "🌤️",  # Mostly sunny
        4: "⛅",  # Partly sunny
        5: "🌥️",  # Mostly cloudy
        6: "☁️",  # Cloudy
        7: "🌥️",  # Overcast
        8: "🌫️",  # Overcast with low clouds
        9: "🌫️",  # Fog
        10: "🌧️",  # Light rain
        11: "🌧️",  # Rain
        12: "🌧️",  # Possible rain
        13: "🌦️",  # Rain shower
        14: "⛈️",  # Thunderstorm
        15: "🌩️",  # Local thunderstorms
        16: "🌨️",  # Light snow
        17: "❄️",  # Snow
        18: "🌨️",  # Possible snow
        19: "🌨️",  # Snow shower
        20: "🌨️🌧️",  # Rain and snow
        21: "🌨️🌧️",  # Possible rain and snow
        22: "🌨️🌧️",  # Rain and snow
        23: "🌧️❄️",  # Freezing rain
        24: "🌧️❄️",  # Possible freezing rain
        25: "🌩️🌨️",  # Hail
        26: "🌙",  # Clear (night)
        27: "🌙🌤️",  # Mostly clear (night)
        28: "🌙⛅",  # Partly clear (night)
        29: "🌙☁️",  # Mostly cloudy (night)
        30: "🌙☁️",  # Cloudy (night)
        31: "🌙🌫️",  # Overcast with low clouds (night)
        32: "🌙🌧️",  # Rain shower (night)
        33: "🌙🌩️",  # Local thunderstorms (night)
        34: "🌙❄️",  # Snow shower (night)
        35: "🌙🌨️🌧️",  # Rain and snow (night)
        36: "🌙🌧️❄️"  # Possible freezing rain (night)
    }

    for index, row in df.iterrows():
        date = index.strftime('%Y-%m-%d')
        icon = weather_icon.get(row["icon"], "❓")
        temp = f'{row["all_day_temperature_max"]:.1f}°C/{row["all_day_temperature_min"]:.1f}°C'
        wind = f'{row["all_day_wind_speed"]:.1f} m/s {row["all_day_wind_dir"]}'
        summary = row["summary"].split('.')[0] if isinstance(row["summary"], str) else row["summary"]

        table_data.append([date, temp, wind, summary, icon])

    headers = ['DATE', 'TEMPERATURE', 'WIND', 'SUMMARY', "ICON"]

    print(tabulate(table_data, headers, tablefmt='presto', colalign=("left",)))

if __name__ == "__main__":
    weather_data()
