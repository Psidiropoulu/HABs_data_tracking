# website/data_app/urls.py
from django.urls import path
from .views import weather_data_view

from .views import skew_t_view, weather_data_view


urlpatterns = [
    path('weather/', weather_data_view, name='weather_data'),
    path('skew_t/', skew_t_view, name='skew_t_view'),
]
