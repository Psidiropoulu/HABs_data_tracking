from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/data/', consumers.RealTimeDataConsumer.as_asgi()),
]