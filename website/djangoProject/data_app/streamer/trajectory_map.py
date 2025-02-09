import folium
from .fetch_sondehub_trajectory import get_sondehub_trajectory

def generate_trajectory_map(launch_lat, launch_lon):
    """
    Generate a Folium map with the SondeHub trajectory.
    """
    data = get_sondehub_trajectory(launch_lat, launch_lon)

    if not data:
        print("No data received from SondeHub API")
        return None

    # Initialize map at launch site
    m = folium.Map(location=[launch_lat, launch_lon], zoom_start=8)

    # Extract trajectory data
    ascent_points = [(p["latitude"], p["longitude"]) for p in data["prediction"][0]["trajectory"]]
    descent_points = [(p["latitude"], p["longitude"]) for p in data["prediction"][1]["trajectory"]]

    print("Ascent Points:", ascent_points)  # <-- ADD THIS LINE
    print("Descent Points:", descent_points)  # <-- ADD THIS LINE

    # Plot ascent trajectory
    folium.PolyLine(ascent_points, color="blue", weight=2.5, opacity=1, tooltip="Ascent Path").add_to(m)

    # Plot descent trajectory
    folium.PolyLine(descent_points, color="red", weight=2.5, opacity=1, tooltip="Descent Path").add_to(m)

    # Add markers
    folium.Marker(ascent_points[0], icon=folium.Icon(color="green"), popup="Launch Site").add_to(m)
    folium.Marker(ascent_points[-1], icon=folium.Icon(color="blue"), popup="Burst Altitude").add_to(m)
    folium.Marker(descent_points[-1], icon=folium.Icon(color="red"), popup="Landing Site").add_to(m)

    return m._repr_html_()
