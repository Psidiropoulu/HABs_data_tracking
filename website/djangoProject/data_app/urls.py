# website/data_app/urls.py
from django.urls import path
from .views import weather_data_view

urlpatterns = [
    path('weather/', weather_data_view, name='weather_data'),
]
