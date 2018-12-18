from django.db import models

# Create your models here.

class Zipcode(models.Model):
    country_iso = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()

class ZipDist(models.Model):
    from_zip_id = models.ForeignKey(Zipcode, on_delete=models.CASCADE, related_name="from_zip_id")
    to_zip_id = models.ForeignKey(Zipcode, on_delete=models.CASCADE, related_name="to_zip_id")
    distance_fly = models.FloatField()
    distance_route = models.FloatField()

    country_iso = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()
