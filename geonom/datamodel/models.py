from django.db import models
import math
from NominatimLibrary import Locator
from random import randrange

# AVERAGE_RATIO is the average ratio dist_route/dist_crow on a random set of postcode.
# When error with normal way, return dist_crow * AVERAGE_RATIO.
#AVERAGE_RATIO = 0.76
AVERAGE_RATIO = 1.0

def average_ratio(dist_crow):
    return dist_crow / AVERAGE_RATIO

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
        return average_ratio(dist_crow)

    # Try getting the distance between two points
    # With first a,b=x,y, then a,b=y,x
    dist = None

    res = DbClass.objects.filter(a_lat = x_lat_grid, a_lon = x_lon_grid, b_lat = y_lat_grid, b_lon = y_lon_grid)
    if len(res) == 0:
        res = DbClass.objects.filter(a_lat = y_lat_grid, a_lon = y_lon_grid, b_lat = x_lat_grid, b_lon = x_lon_grid)

        if len(res) == 0:
            # raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
            try:
                step = DbClass.get_step()
                x_grid = ((x_lat_grid+0.5) * step,(x_lon_grid+0.5) * step)
                y_grid = ((y_lat_grid+0.5) * step,(y_lon_grid+0.5) * step)
                d_route = locator.distance_route_coords(x_grid,y_grid)
                d_crow = locator.distance_crow_coords(x_grid,y_grid)

                new_line = DbClass(x_lat_grid,x_lon_grid,y_lat_grid,y_lon_grid,d_crow,d_route)
                new_line.save()

                return dist_crow * float(d_route) / d_crow
            except Exception as e:
                return average_ratio(dist_crow)
        else:
            dist = res[0]
    else:
        dist = res[0]

    ratio = float(dist.distance_route) / dist.distance_fly

    return ratio * dist_crow

# Create your models here.

class Zipcode(models.Model):
    country_iso = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=30)
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

    def get_step():
        return 1.0

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

    def get_step():
        return 0.1

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
            return average_ratio(dist_crow)

        # Try getting the distance between two points
        # With first a,b=x,y, then a,b=y,x
        dist = None

        res = ZipDist_2digits.objects.filter(a_country_2digits = x_country_2digits, b_country_2digits = y_country_2digits)
        if len(res) == 0:
            res = ZipDist_2digits.objects.filter(a_country_2digits = y_country_2digits, b_country_2digits = x_country_2digits)

            if len(res) == 0:
                # raise NotFoundException((postcode_x, countrycode_x, postcode_y, countrycode_y))
                return average_ratio(dist_crow)
            else:
                dist = res[0]
        else:
            dist = res[0]

        ratio = float(dist.distance_route) / dist.distance_fly

        return ratio * dist_crow

def test_distances_dbs(nb_tests):
    TABLE = "%15s | %2s | %15s | %2s || %5s || %3s | %3s | %3s | %3s |"

    zipcodes = Zipcode.objects.all();
    nb_zipcodes = len(zipcodes)

    locator = Locator()


    print(TABLE % ("x_zip","xc","y_zip","yc", "route", "cro", "gr1", "g10", "2di"))
    print(TABLE % ("","","","","","","","",""))

    avg_cro = []
    avg_gr1 = []
    avg_g10 = []
    avg_2di = []

    err_count = 0
    f = open("tests_" + str(AVERAGE_RATIO) + ".csv", mode="w")

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

            avg_cro.append(dpcro)
            avg_gr1.append(dpgr1)
            avg_g10.append(dpg10)
            avg_2di.append(dp2di)

            print(TABLE % (zc_x.zip_code,zc_x.country_iso,zc_y.zip_code, zc_y.country_iso, math.floor(dist_route), dpcro, dpgr1, dpg10, dp2di))
            f.write("%s,%s,%s,%s\n" % (dpcro, dpgr1, dpg10, dp2di))
        except Exception as e:
            print((TABLE + " error getting route") % (zc_x.zip_code,zc_x.country_iso,zc_y.zip_code, zc_y.country_iso, "", "", "", "", ""))
            err_count += 1


    nb_t_final = nb_tests - err_count
    print(TABLE % ("","","","","","","","",""))
    print(TABLE % ("","","","","", int(sum(avg_cro)/nb_t_final), int(sum(avg_gr1)/nb_t_final), int(sum(avg_g10)/nb_t_final), int(sum(avg_2di)/nb_t_final)))

    print("Number of errors with Graphhopper : " + str(err_count) + " , " + str(int(err_count * 100 / nb_tests)) + "%.")
