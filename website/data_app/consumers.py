#handing websockets connections and pushing real-time updates to the frondtend 

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RealTimeData
from .serializers import RealTimeDataSerializer

class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        data = RealTimeData.objects.last()
        if data:
            serializer = RealTimeDataSerializer(data)
            await self.send(text_data=json.dumps(serializer.data))

    async def receive(self, text_data):
        data = RealTimeData.objects.last()
        serializer = RealTimeDataSerializer(data)
        await self.send(text_data=json.dumps(serializer.data))


class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Send the latest data on connect
        data = await self.get_latest_data()
        if data:
            await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        # Parse incoming data
        data = json.loads(text_data)
        # Save the received data
        await self.save_data(data)
        # Send the latest data to all connected clients
        latest_data = await self.get_latest_data()
        await self.send(text_data=json.dumps(latest_data))

    async def get_latest_data(self):
        # Get the latest data asynchronously
        latest_data = await RealTimeData.objects.alast('timestamp')
        if latest_data:
            serializer = RealTimeDataSerializer(latest_data)
            return serializer.data
        return {}

    async def save_data(self, data):
        # Save the received data to the database asynchronously
        await RealTimeData.objects.acreate(
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            altitude=data.get('altitude'),
            speed=data.get('speed'),
            direction=data.get('direction'),
            temperature=data.get('temperature'),
            pressure=data.get('pressure'),
            humidity=data.get('humidity'),
            no2we=data.get('no2we'),
            no2ae=data.get('no2ae'),
            muon_count=data.get('muon_count'),
            muon_rate=data.get('muon_rate'),
            flight_mode=data.get('flight_mode')
        )