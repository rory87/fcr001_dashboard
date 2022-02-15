from django.db import models
from djgeojson.fields import PointField, PolygonField, LineStringField

class load(models.Model):
    network = models.IntegerField()
    feeder = models.IntegerField()
    geom = PointField(null=True, blank=True)

class cable(models.Model):
    network = models.IntegerField()
    feeder = models.IntegerField()
    geom = LineStringField(null=True, blank=True)

class sub(models.Model):
    network = models.IntegerField()
    feeder = models.IntegerField()
    geom = PolygonField(null=True, blank=True)

class pillar(models.Model):
    network = models.IntegerField()
    feeder = models.IntegerField()
    geom = PolygonField(null=True, blank=True)









