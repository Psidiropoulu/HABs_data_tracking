from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealTimeData
from .serializers import RealTimeDataSerializer
from django.http import JsonResponse
#from .streamer.read_sensors import fetch_sensor_data
from .models import WeatherData
from .streamer.skewT_logP import generate_skew_t_base


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

def skew_t_view(request):
    # Default (Norfolk) or user-provided latitude and longitude
    latitude = float(request.GET.get('latitude', 52.63))
    longitude = float(request.GET.get('longitude', 1.30))

    # Generate the base Skew-T diagram
    base_image = generate_skew_t_base(latitude, longitude)

    # Render the diagram in the template
    return render(request, 'data_app/skew_t.html', {
        'base_image': base_image,
        'latitude': latitude,
        'longitude': longitude,
    })
