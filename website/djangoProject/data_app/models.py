from django.db import models

class RealTimeData(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)