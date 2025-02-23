from django.db import models

# Create your models here.


# Model to use the date from the STATE file, but only using the parameters that we need for our new model
class TrajectoryData(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    direction = models.FloatField(null=True, blank=True)
    flight_mode = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Trajectory: {self.timestamp}: {self.latitude}, {self.longitude}, {self.altitude}"