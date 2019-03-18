from django.db import models
import math
from NominatimLibrary import Locator
from random import randrange

class NotFoundException(Exception):
    pass

def distance_between_postcodes_grid(DbClass, postcode_x, countrycode_x, postcode_y, countrycode_y):
    # Transform postcodes into coordinates :
    (x_lat, x_lon, x_lat_grid, x_lon_grid) = DbClass.get_latlon_grid(postcode_x, countrycode_x)
    (y_lat, y_lon, y_lat_grid, y_lon_grid) = DbClass.get_latlon_grid(postcode_y, countrycode_y)

    # Distance crow :
    locator = Locator()
    dist_crow = locator.distance_crow_coords((x_lat,x_lon),(y_lat,y_lon))

    if x_lat_grid == y_lat_grid and x_lon_grid == y_lon_grid:
        return dist_crow

    # Try getting the distance between two points
    # With first a,b=x,y, then a,b=y,x
    dist = None

    res = DbClass.objects.filter(a_lat = x_lat_grid, a_lon = x_lon_grid, b_lat = y_lat_grid, b_lon = y_lon_grid)
    if len(res) == 0:
        res = DbClass.objects.filter(a_lat = y_lat_grid, a_lon = y_lon_grid, b_lat = x_lat_grid, b_lon = x_lon_grid)

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
    """
       this will be printed when when calling an object of ZipDist
    """
    def __str__(self):
        return "Distance as the crow flies: " + str(self.distance_fly)

    def get_latlon_grid(postcode, countrycode):
        zipcode = Zipcode.objects.get(country_iso=countrycode, zip_code=postcode)
        lat = zipcode.lat
        lon = zipcode.lon
        lat_grid = math.floor(lat)
        lon_grid = math.floor(lon)
        return (lat, lon, lat_grid, lon_grid)

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        return distance_between_postcodes_grid(ZipDist, postcode_x, countrycode_x, postcode_y, countrycode_y)

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

    def get_latlon_grid(postcode, countrycode):
        zipcode = Zipcode.objects.get(country_iso=countrycode, zip_code=postcode)
        lat = zipcode.lat
        lon = zipcode.lon
        lat_grid = math.floor(lat * 10)
        lon_grid = math.floor(lon * 10)
        return (lat, lon, lat_grid, lon_grid)

    def distance_between_postcodes(postcode_x, countrycode_x, postcode_y, countrycode_y):
        return distance_between_postcodes_grid(ZipDist_grid_10, postcode_x, countrycode_x, postcode_y, countrycode_y)

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
        locator = Locator()
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

def test_distances_dbs(nb_tests):
    zipcodes = Zipcode.objects.all();
    nb_zipcodes = len(zipcodes)

    locator = Locator()


    print("%7s,%2s | %7s,%2s | %5s | %3s | %3s | %3s | %3s" % ("x_zip","xc","y_zip","yc", "route", "cro", "gr1", "g10", "2di"))

    avg_cro = 0
    avg_gr1 = 0
    avg_g10 = 0
    avg_2di = 0

    err_count = 0

    for i in range(nb_tests):
        zc_x = zipcodes[randrange(nb_zipcodes)]
        zc_y = zipcodes[randrange(nb_zipcodes)]

        dist_crow = locator.distance_crow_coords((zc_x.lat,zc_x.lon),(zc_y.lat,zc_y.lon))
        dist_route = None
        try:
            dist_route = locator.distance_route_coords((zc_x.lat,zc_x.lon),(zc_y.lat,zc_y.lon))

            dist_grid_1 = ZipDist.distance_between_postcodes(zc_x.zip_code, zc_x.country_iso, zc_y.zip_code, zc_y.country_iso)
            dist_grid_10 = ZipDist_grid_10.distance_between_postcodes(zc_x.zip_code, zc_x.country_iso, zc_y.zip_code, zc_y.country_iso)
            dist_2digits = ZipDist_2digits.distance_between_postcodes(zc_x.zip_code, zc_x.country_iso, zc_y.zip_code, zc_y.country_iso)

            distPercent = lambda d: math.floor(d * 100/float(dist_route))

            dpcro  = distPercent(dist_crow)
            dpgr1  = distPercent(dist_grid_1)
            dpg10  = distPercent(dist_grid_10)
            dp2di  = distPercent(dist_2digits)

            avg_cro += dpcro
            avg_gr1 += dpgr1
            avg_g10 += dpg10
            avg_2di += dp2di

            print("%7s,%2s | %7s,%2s | %5s | %3s | %3s | %3s | %3s" % (zc_x.zip_code,zc_x.country_iso,zc_y.zip_code, y.country_iso, dist_route, dpcro, dpgr1, dpg10, dp2di))
        except Exception as e:
            err_count += 1


    nb_t_final = nb_tests - err_count
    print("%7s,%2s | %7s,%2s | %5s | %3s | %3s | %3s | %3s" % ("","","","","", avg_cro/nb_t_final, dpgr1/nb_t_final, dpg10/nb_t_final, dp2di/nb_t_final))

    print("Number of errors with Graphhopper : " + str(err_count) + " , " + str (err_count * 100 / nb_tests))
