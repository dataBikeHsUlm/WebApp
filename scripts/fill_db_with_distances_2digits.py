#!/bin/env python3
from NominatimLibrary import Locator, NotFoundException
import psycopg2
import mysql.connector
import sys
import math

# Europe limits :
LON_MIN = -11
LON_MAX = 41
LAT_MIN = 35
LAT_MAX = 71
CENTROID_SHIFT = 0.5

# MySQL
DB_MySQL_NAME = "geonom"
DB_MySQL_USER = "admin"
DB_MySQL_TABLE_ZIP = "datamodel_zipcode"
DB_MySQL_TABLE_DIST = "datamodel_zipdist_2digits"
INSERT_INTO_MYSQL = "INSERT INTO " + DB_MySQL_TABLE_DIST + " VALUES (id, %s, %s, %s, %s);"

QUERY_POSTCODES_COUNTRIES = "SELECT * FROM " + DB_MySQL_TABLE_ZIP + ";"

print(" --------------------------------- ")
DB_MySQL_PASSWORD = input("MySQL password : ")

locator = Locator()

def connect_mydb():
    print("Connecting to MySQL database...")
    mydb = mysql.connector.connect(
            host="localhost",
            user=DB_MySQL_USER,
            passwd=DB_MySQL_PASSWORD,
            database=DB_MySQL_NAME
    )
    return (mydb, mydb.cursor())

(mydb, mydb_cursor) = connect_mydb()

print("Executing query to get all postcodes per countries...")
mydb_cursor.execute(QUERY_POSTCODES_COUNTRIES)
elms = mydb_cursor.fetchall()

print("Filtering squares containing postcodes...")

res = {}
for city in elms:
    country = city[1]
    zipcode = city[2]
    country_2digits = country + zipcode[:2]

    # We still use the lat and lon to filter european cities and calculate centroid
    lat = city[3]
    lon = city[4]
    if lat >= LAT_MIN and lat <= LAT_MAX and lon >= LON_MIN and lon <= LON_MAX:
        points = res.get(country_2digits) or []
        points.append((lat,lon))

        res[country_2digits] = points

keys = res.keys()

print("Calculating average centroid of each area...")
for key in keys:
    points = res[key]

    # Calculate average point :
    lats, lons = zip(*points)
    n = float(len(lats))
    avg_lats,avg_lons = sum(lats)/n,sum(lons)/n
    avg_point = (avg_lats,avg_lons)

    # Sort points by distance to the centroid :
    calc_dist = lambda point: math.sqrt(float(avg_lats-point[0])**2 + float(avg_lons-point[0])**2)
    sorted_points = sorted(points, key=calc_dist)

    sorted_points.insert(0,(avg_lats, avg_lons))
    final_point = None

    # Find the first working point :
    for point in sorted_points:
        if locator.is_usable_point_graphhopper(point):
            final_point = point
            break

    if final_point == None:
        print("ERROR : Couldn't find a working point for Graphhopper for key : " + str(key), file=sys.stderr)
        del res[key]
    else:
        res[key] = final_point

keys = res.keys()
print("We are using " + str(len(keys)) + " areas.")
nb_paths = math.factorial(len(keys))/(math.factorial(2)*math.factorial(len(keys)-2))
print("This makes a total number of paths of : " + str(nb_paths))

print("Calculating distances between areas...")
counter = 0

for (a_id, a_country_2digits) in enumerate(keys):
    a_coords = res[a_country_2digits]
    for (b_id, b_country_2digits) in enumerate(keys):
        if b_id <= a_id:
            continue

        counter += 1

        b_coords = res[b_country_2digits]

        d_crow = locator.distance_crow_coords(a_coords, b_coords);

        try:
            d_route = locator.distance_route_coords(a_coords, b_coords);
        except Exception as e:
            counter -= 1
            print("ERROR : getting distance by route : " + str(a_country_2digits) + "," + str(b_country_2digits) + "," + str(a_coords) + "," + str(b_coords) + " : " + str(e), file=sys.stderr)
            if e.errno == 2055:
                (mydb, mydb_cursor) = connect_mydb()
            continue

        try:
            mydb_cursor.execute(INSERT_INTO_MYSQL, [a_country_2digits, b_country_2digits, d_crow, d_route])
            mydb.commit()
        except Exception as e:
            counter -= 1
            print("ERROR : inserting in db : " + str(a_country_2digits) + "," + str(b_country_2digits) + "," + str(a_coords) + "," + str(b_coords) + " : " + str(e), file=sys.stderr)
            continue

print("Stopped at zipcode nb : " + str(counter))
