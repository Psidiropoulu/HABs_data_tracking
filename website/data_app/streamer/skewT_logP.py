import requests
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units
import numpy as np
from io import BytesIO
import base64

def generate_skew_t_base(latitude, longitude):
    """Generate the base Skew-T diagram with API-predicted data."""
    # Step 1: Fetch API data
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&hourly="
        f"temperature_1000hPa,temperature_975hPa,temperature_950hPa,temperature_925hPa,"
        f"temperature_900hPa,temperature_850hPa,temperature_800hPa,temperature_700hPa,"
        f"temperature_600hPa,temperature_500hPa,temperature_400hPa,temperature_300hPa,"
        f"temperature_250hPa,temperature_200hPa,temperature_150hPa,temperature_100hPa,"
        f"temperature_70hPa,temperature_50hPa,temperature_30hPa,"
        f"relative_humidity_1000hPa,relative_humidity_975hPa,relative_humidity_950hPa,"
        f"relative_humidity_925hPa,relative_humidity_900hPa,relative_humidity_850hPa,"
        f"relative_humidity_800hPa,relative_humidity_700hPa,relative_humidity_600hPa,"
        f"relative_humidity_500hPa,relative_humidity_400hPa,relative_humidity_300hPa,"
        f"relative_humidity_250hPa,relative_humidity_200hPa,relative_humidity_150hPa,"
        f"relative_humidity_100hPa,relative_humidity_70hPa,relative_humidity_50hPa,"
        f"relative_humidity_30hPa"
    )

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

    # Step 2: Prepare API data
    pressure_levels = [
        1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30
    ] * units.hPa
    temperature = [
        data["hourly"][f"temperature_{level}hPa"][0] for level in pressure_levels.magnitude
    ] * units.degC
    relative_humidity = [
        data["hourly"][f"relative_humidity_{level}hPa"][0] for level in pressure_levels.magnitude
    ]

    # Calculate dew point using Magnus-Tetens formula
    B, C = 17.62, 243.12
    dew_point = [
        (C * (np.log(rh / 100) + (B * t.magnitude) / (C + t.magnitude))) /
        (B - (np.log(rh / 100) + (B * t.magnitude) / (C + t.magnitude)))
        for t, rh in zip(temperature, relative_humidity)
    ] * units.degC

    # Step 3: Plot the base Skew-T diagram
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=45)
    skew.plot(pressure_levels, temperature, 'r', label="Temperature")
    skew.plot(pressure_levels, dew_point, 'g', label="Dew Point")
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    skew.ax.legend(loc='upper right')
    skew.ax.set_ylim(1000, 30)
    skew.ax.set_xlim(-80, 40)
    plt.title("Skew-T Log-P Diagram (Base Data)")
    # plt.show()

    # Save to base64 for embedding
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded_image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return encoded_image


# # test
# image = generate_skew_t_base(53.12, 1.23)
