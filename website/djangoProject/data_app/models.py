from django.db import models


class RealTimeData(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)


from django.db import models

class WeatherData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    visibility = models.IntegerField()
    cloud_coverage = models.IntegerField()
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()

    def __str__(self):
        return f"Weather Data at {self.timestamp}"
