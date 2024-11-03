from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RealTimeData
from .serializers import RealTimeDataSerializer
from django.shortcuts import render

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
        
def display_data(request):
    return render(request, 'data_app/display_data.html')