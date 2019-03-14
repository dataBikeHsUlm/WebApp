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
    """
       this will be printed when when calling an object of ZipDist
    """
    def __str__(self):
        return "Distance as the crow flies: " + str(self.distance_fly)

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
                # raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
                return dist_crow
            else:
                dist = res[0]
        else:
            dist = res[0]

        ratio = float(dist.distance_route) / dist.distance_fly

        return ratio * dist_crow

class ZipDist_2digits(models.Model):
    """
        *_country_2digits, the name of the country followed by the two digits : 'DE08'
    """
    a_country_2digits = models.CharField(max_length=4)
    b_country_2digits = models.CharField(max_length=4)
    distance_fly = models.FloatField()
    distance_route = models.FloatField()

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        # Transform postcodes into coordinates :
        x_zipcode = Zipcode.objects.get(country_iso=countrycode_x, zip_code=postcode_x)
        x_lat = x_zipcode.lat
        x_lon = x_zipcode.lon
        x_country_2digits = countrycode_x + postcode_x[:2]

        y_zipcode = Zipcode.objects.get(country_iso=countrycode_y, zip_code=postcode_y)
        y_lat = y_zipcode.lat
        y_lon = y_zipcode.lon
        y_country_2digits = countrycode_y + postcode_y[:2]

        # Distance crow :
        locator = NominatimLibrary.Locator()
        dist_crow = locator.distance_crow_coords((x_lat,x_lon),(y_lat,y_lon))

        if x_country_2digits == y_country_2digits:
            return dist_crow

        # Try getting the distance between two points
        # With first a,b=x,y, then a,b=y,x
        dist = None

        res = ZipDist_2digits.objects.filter(a_country_2digits = x_country_2digits, b_country_2digits = y_country_2digits)
        if len(res) == 0:
            res = ZipDist_2digits.objects.filter(a_country_2digits = y_country_2digits, b_country_2digits = x_country_2digits)

            if len(res) == 0:
                # raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
                return dist_crow
            else:
                dist = res[0]
        else:
            dist = res[0]

        ratio = float(dist.distance_route) / dist.distance_fly

        return ratio * dist_crow
