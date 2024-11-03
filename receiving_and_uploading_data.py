# models.py
from django.db import models

class RealTimeData(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)


# serializers.py
from rest_framework import serializers
from .models import RealTimeData

class RealTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = '__all__'

# views.py
from rest_framework import viewsets
from .models import RealTimeData
from .serializers import RealTimeDataSerializer

class RealTimeDataViewSet(viewsets.ModelViewSet):
    queryset = RealTimeData.objects.all()
    serializer_class = RealTimeDataSerializer

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RealTimeDataViewSet

router = DefaultRouter()
router.register(r'data', RealTimeDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]


# Raspberry Pi Script (e.g., send_data.py)
import requests
import random
import time

API_URL = "http://your-server-ip/api/data/"
headers = {"Content-Type": "application/json"}

while True:
    data = {
        "value": random.randint(0, 100)  # Replace with actual sensor data
    }
    response = requests.post(API_URL, json=data, headers=headers)
    print("Data sent:", response.json())
    time.sleep(5)  # Send data every 5 seconds


# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import RealTimeData
from .serializers import RealTimeDataSerializer

class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Load initial data
        data = RealTimeData.objects.last()
        if data:
            serializer = RealTimeDataSerializer(data)
            await self.send(text_data=json.dumps(serializer.data))

    async def receive(self, text_data):
        # Fetch and send updated data to all connected clients
        data = RealTimeData.objects.last()
        serializer = RealTimeDataSerializer(data)
        await self.send(text_data=json.dumps(serializer.data))


const socket = new WebSocket("ws://your-server-ip/ws/data/");

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    document.getElementById("data-value").innerText = data.value;
};