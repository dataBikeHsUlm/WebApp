from django.db import models
import math
import NominatimLibrary

class NotFoundException(Exception):
    pass

def distance_between_postcodes_grid(db_class, function_calc_id, postcode_x, countrycode_x, postcode_y, countrycode_y):
    # Transform postcodes into coordinates :
    (x_lat, x_lon, x_lat_grid, x_lon_grid) = function_calc_id(postcode_x, countrycode_x)
    (y_lat, y_lon, y_lat_grid, y_lon_grid) = function_calc_id(postcode_y, countrycode_y)

    # Distance crow :
    locator = NominatimLibrary.Locator()
    dist_crow = locator.distance_crow_coords((x_lat,x_lon),(y_lat,y_lon))

    if x_lat_grid == y_lat_grid and x_lon_grid == y_lon_grid:
        return dist_crow

    # Try getting the distance between two points
    # With first a,b=x,y, then a,b=y,x
    dist = None

    res = db_class.objects.filter(a_lat = x_lat_grid, a_lon = x_lon_grid, b_lat = y_lat_grid, b_lon = y_lon_grid)
    if len(res) == 0:
        res = db_class.objects.filter(a_lat = y_lat_grid, a_lon = y_lon_grid, b_lat = x_lat_grid, b_lon = x_lon_grid)

        if len(res) == 0:
            # raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
            return dist_crow
        else:
            dist = res[0]
    else:
        dist = res[0]

    ratio = float(dist.distance_route) / dist.distance_fly

    return ratio * dist_crow

# Create your models here.

class Zipcode(models.Model):
    country_iso = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()

class ZipDist(models.Model):
    """
        these are the coordinates of the north-west-hand corner of the "square", with grid of 1°
    """
    a_lat = models.IntegerField()
    a_lon = models.IntegerField()
    b_lat = models.IntegerField()
    b_lon = models.IntegerField()
    distance_fly = models.FloatField()
    distance_route = models.FloatField()

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        f = lambda postcode, countrycode:
            zipcode = Zipcode.objects.get(country_iso=countrycode, zip_code=postcode)
            lat = zipcode.lat
            lon = zipcode.lon
            lat_grid = math.floor(lat)
            lon_grid = math.floor(lon)
            return (lat, lon, lat_grid, lon_grid)

        return distance_between_postcodes_grid(ZipDist, f, postcode_x, countrycode_x, postcode_y, countrycode_y)

class ZipDist_grid_10(models.Model):
    """
        these are the coordinates of the north-west-hand corner of the "square", with grid of 0.1°
    """
    a_lat = models.IntegerField()
    a_lon = models.IntegerField()
    b_lat = models.IntegerField()
    b_lon = models.IntegerField()
    distance_fly = models.FloatField()
    distance_route = models.FloatField()

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        f = lambda postcode, countrycode:
            zipcode = Zipcode.objects.get(country_iso=countrycode, zip_code=postcode)
            lat = zipcode.lat
            lon = zipcode.lon
            lat_grid = math.floor(lat * 10)
            lon_grid = math.floor(lon * 10)
            return (lat, lon, lat_grid, lon_grid)

        return distance_between_postcodes_grid(ZipDist_grid_10, f, postcode_x, countrycode_x, postcode_y, countrycode_y)

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
