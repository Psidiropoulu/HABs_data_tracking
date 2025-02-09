import requests
import datetime

def get_sondehub_trajectory(launch_lat, launch_lon):

    current_time = datetime.datetime.utcnow()
    launch_time = current_time + datetime.timedelta(minutes=30)  # Set launch 30 min from now
    launch_time_iso = launch_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    API_URL = "https://api.v2.sondehub.org/tawhiri"

    params = {
        "launch_latitude": launch_lat,  # Example: 52.2135
        "launch_longitude": launch_lon,  # Example: 0.0964
        "launch_datetime": launch_time_iso,
        "ascent_rate": 5,  # m/s
        "burst_altitude": 30000,  # 30 km burst altitude
        "descent_rate": 5,  # m/s
    }

    print("Sending API request to:", API_URL)
    print("Parameters:", params)

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Success! Trajectory Data Received")
        print("Trajectory Data:", data)
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

