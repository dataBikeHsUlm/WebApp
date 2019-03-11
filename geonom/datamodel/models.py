from django.db import models
import math
import NominatimLibrary

class NotFoundException(Exception):
    pass

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
    a_lat = models.IntegerField()
    a_lon = models.IntegerField()
    b_lat = models.IntegerField()
    b_lon = models.IntegerField()
    distance_fly = models.FloatField()
    distance_route = models.FloatField()

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        # Transform postcodes into coordinates :
        x_zipcode = Zipcode.objects.get(country_iso=countrycode_x, zip_code=postcode_x)
        x_lat = x_zipcode.lat
        x_lon = x_zipcode.lon

        y_zipcode = Zipcode.objects.get(country_iso=countrycode_y, zip_code=postcode_y)
        y_lat = y_zipcode.lat
        y_lon = y_zipcode.lon

        # Distance crow :
        locator = NominatimLibrary.Locator()
        dist_crow = locator.distance_crow_coords((x_lat,x_lon),(y_lat,y_lon))

        # Normalize the coordinates to match the grid :
        x_lat_floored = math.floor(x_lat)
        x_lon_floored = math.floor(x_lon)
        y_lat_floored = math.floor(y_lat)
        y_lon_floored = math.floor(y_lon)

        if x_lat_floored == y_lat_floored and x_lon_floored == y_lon_floored:
            return dist_crow

        # Try getting the distance between two points
        # With first a,b=x,y, then a,b=y,x
        dist = None

        res = ZipDist.objects.filter(a_lat = x_lat_floored, a_lon = x_lon_floored, b_lat = y_lat_floored, b_lon = y_lon_floored)
        if len(res) == 0:
            res = ZipDist.objects.filter(a_lat = y_lat_floored, a_lon = y_lon_floored, b_lat = x_lat_floored, b_lon = x_lon_floored)

            if len(res) == 0:
                raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
            else:
                dist = res[0]
        else:
            dist = res[0]

        ratio = float(dist.distance_route) / dist.distance_fly

        return ratio * dist_crow
