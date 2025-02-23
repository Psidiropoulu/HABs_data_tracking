# website/data_app/urls.py

from django.urls import path
from .views import weather_data_view, submit_data_view, weather_view, skew_t_view, trajectory_view, index
from django.urls import path, include

urlpatterns = [
    path('weather/', weather_data_view, name='weather_data'),
    path('live_weather/', weather_view, name='weather_view'),
    path('skew_t/', skew_t_view, name='skew_t_view'),
    path('trajectory/', trajectory_view, name='trajectory_view'),
    path('api/addData', submit_data_view, name='submit_data'),  # Keeping both changes
    path('data/', include('data_app.urls')),
    path('', index, name='index'),
]
