import subprocess
import json

def read_bme_sensor():
    try:
        output = subprocess.run(["./sensors/bme"], capture_output=True, text=True, check=True)

        if not output.stdout.strip().startswith("{"):
            print(f"Unexpected output from BME sensor: {output.stdout.strip()}")
            return None

        sensor_data = json.loads(output.stdout.strip())
        return sensor_data

    except Exception as e:
        print(f"Error reading BME sensor: {e}")
        return None
