from django.db import models

# Create your models here.

class Zipcode(models.Model):
    country_iso = models.CharField(max_lenght=2)
    zip_code = models.CharField(max_lenght=10)
    lat = models.FloatField()
    lon = models.FloatField()

class ZipDist(models.Model):
    from_zip_id = models.ForeignKey(Zipcode, on_delete=models.CASCADE)
    to_zip_id = models.ForeignKey(Zipcode, on_delete=models.CASCADE)
    distance_fly = models.FloatField()
    distance_route = models.FloatField()
