"""
import ctypes

# Load the shared library (use the correct path to the compiled .so file)
sensors_lib = ctypes.CDLL('/path/to/sensors.so')  # Replace with the actual path

# Define argument and return types for the functions (modify as needed)
sensors_lib.read_bme_data.restype = ctypes.c_float  # Example function
sensors_lib.read_gps_data.restype = ctypes.c_char_p  # Example function

def fetch_sensor_data():
    bme_data = sensors_lib.read_bme_data()
    gps_data = sensors_lib.read_gps_data().decode('utf-8')

    print("BME Data:", bme_data)
    print("GPS Data:", gps_data)

    return {
        "bme_data": bme_data,
        "gps_data": gps_data
    }
"""