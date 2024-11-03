from django.urls import path
from .views import LoRaWANDataView

urlpatterns = [
    path('api/data/', LoRaWANDataView.as_view(), name='lorawan-data'),
    path('display/', display_data, name='display_data'),
]