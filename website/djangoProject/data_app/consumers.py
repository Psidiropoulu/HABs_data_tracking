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