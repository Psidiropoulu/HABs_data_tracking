# website/data_app/urls.py
from django.urls import path
from .views import display_data, LoRaWANDataView  # Ensure both views are imported correctly

urlpatterns = [
    path('api/data/', LoRaWANDataView.as_view(), name='lorawan-data'),
    path('display/', display_data, name='display_data'),
]