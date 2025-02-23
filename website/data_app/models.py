from django.db import models


class RealTimeData(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    
    #added new fields so that the data from the sensors can be saved into the RealTimeData (so, the file structure is the same as that of the STATE from main.h)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    direction = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    no2we = models.FloatField(null=True, blank=True)
    no2ae = models.FloatField(null=True, blank=True)
    muon_count = models.IntegerField(null=True, blank=True)
    muon_rate = models.FloatField(null=True, blank=True)
    flight_mode = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp}: {self.latitude}, {self.longitude}, {self.altitude}"



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
