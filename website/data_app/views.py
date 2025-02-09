from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealTimeData
from .serializers import RealTimeDataSerializer
from django.http import JsonResponse
#from .streamer.read_sensors import fetch_sensor_data
from .models import WeatherData
<<<<<<< HEAD:website/djangoProject/data_app/views.py
from .streamer.skewT_logP import generate_skew_t_base
from .streamer.import_weather_data2 import get_weather
from django.http import JsonResponse
import pandas as pd
from .streamer.trajectory_map import generate_trajectory_map
from django.http import JsonResponse
=======
import json
>>>>>>> origin/main:website/data_app/views.py


'''
class LoRaWANDataView(APIView):
    def post(self, request):
        try:
            data_value = request.data.get('uplink_message', {}).get('decoded_payload', {}).get('value')
            if data_value is not None:
                data_instance = RealTimeData.objects.create(value=data_value)
                serializer = RealTimeDataSerializer(data_instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''
    
# Make sure display_data is defined
def display_data(request):
    return render(request, 'data_app/display_data.html')

#def sensor_data_view(request):
#    data = fetch_sensor_data()
#    return JsonResponse(data)

def weather_data_view(request):
    latest_weather = WeatherData.objects.order_by('-timestamp').first()
    context = {
        'weather': latest_weather
    }
    return render(request, 'data_app/weather_template.html', context)

def submit_data_view(APIView):
    def post(self, request):
        value = json.loads(request.data)
        print(value)
        try:
            data_instance = RealTimeData.objects.create(**value)
            data_instance.save()
        except Exception as e:
            print(str(e))

def weather_view(request):

    latitude = float(request.GET.get('latitude', 53.12))  # Default lat
    longitude = float(request.GET.get('longitude', 1.23))  # Default lon

    summary, icon, temp, precipitation, wind_speed, wind_direction, cloud_cover, df_hourly, df_daily = get_weather(latitude, longitude)

    if not df_hourly.empty:
        df_hourly['time'] = pd.to_datetime(df_hourly.index).strftime('%H:%M %p')

    if not df_daily.empty:
        df_daily['date'] = pd.to_datetime(df_daily.index).strftime('%Y-%m-%d')

    context = {
        'latitude': latitude,
        'longitude': longitude,
        'summary': summary,
        'icon': icon,
        'temperature': temp,
        'precipitation': precipitation,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'cloud_cover': cloud_cover,
        'hourly_data': df_hourly.to_dict(orient="records"),  # Convert to list of dicts
        'daily_data': df_daily.to_dict(orient="records"),
    }

    return render(request, 'data_app/weather_page.html', context)


def skew_t_view(request):
    latitude = float(request.GET.get('latitude', 52.63))
    longitude = float(request.GET.get('longitude', 1.30))

    base_image = generate_skew_t_base(latitude, longitude)

    return render(request, 'data_app/skew_t.html', {
        'base_image': base_image,
        'latitude': latitude,
        'longitude': longitude,
    })


def trajectory_view(request):
    launch_lat = 52.2135
    launch_lon = 0.0964

    trajectory_map = generate_trajectory_map(launch_lat, launch_lon)

    if not trajectory_map:
        print("Map generation failed!")

    return render(request, "data_app/trajectory.html", {"trajectory_map": trajectory_map})