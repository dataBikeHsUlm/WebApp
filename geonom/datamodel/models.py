from django.db import models

# Create your models here.

class Zipcode(models.Model):
    country_iso = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()

class ZipDist(models.Model):
    """
        these are the coordinates of the north-west-hand corner of the "square"
    """
    a_lat = models.IntField()
    a_lon = models.IntField()
    b_lat = models.IntField()
    b_lon = models.IntField()
    distance_fly = models.FloatField()
    distance_route = models.FloatField()
