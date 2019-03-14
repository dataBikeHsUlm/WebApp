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
        prev_sums = res.get(country_2digits)

        n,sum_lat,sum_lon = (0,0,0)
        if prev_sums != None:
            n,sum_lat,sum_lon = prev_sums
            
        res[country_2digits] = (n+1,sum_lat+lat,sum_lon+lon)

keys = res.keys()
print("We are using " + str(len(keys)) + " areas.")
nb_paths = math.factorial(len(keys))/(math.factorial(2)*math.factorial(len(keys)-2))
print("This makes a total number of paths of : " + str(nb_paths))

print("Calculating average centroid of each area...")
for key in keys:
    n,sum_lat,sum_lon = res[key]
    res[key] = (float(sum_lat)/n,float(sum_lon)/n)

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
