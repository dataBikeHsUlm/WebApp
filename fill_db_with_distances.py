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
DB_MySQL_TABLE_DIST = "datamodel_zipdist"
INSERT_INTO_MYSQL = "INSERT INTO " + DB_MySQL_TABLE_DIST + " VALUES (id, %s, %s, %s, %s, %s, %s);"

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
    lat = math.floor(city[3])
    lon = math.floor(city[4])
    if lat >= LAT_MIN and lat <= LAT_MAX and lon >= LON_MIN and lon <= LON_MAX:
        res[(lat,lon)] = True

keys = res.keys()
print("We are using " + str(len(keys)) + " instead of " + str((LON_MAX-LON_MIN)*(LAT_MAX-LAT_MIN)))
nb_paths = math.factorial(len(keys))/(math.factorial(2)*math.factorial(len(keys)-2))
print("This makes a total number of paths of : " + str(nb_paths))

print("Calculating distances between squares...")
counter = 0

for (a_id, a_square) in enumerate(keys):
    for (b_id, b_square) in enumerate(keys[a_id+1:]):
        counter += 1

        a_coords = (a_square[0] + CENTROID_SHIFT, a_square[1] + CENTROID_SHIFT)
        b_coords = (b_square[0] + CENTROID_SHIFT, b_square[1] + CENTROID_SHIFT)

        d_crow = locator.distance_crow_coords(a_coords, b_coords);

        try:
            d_route = locator.distance_route_coords(a_coords, b_coords);
        except Exception as e:
            print("ERROR : getting distance by route : " + str(e), file=sys.stderr)
            if e.errno == 2055:
                (mydb, mydb_cursor) = connect_mydb()
            continue

        try:
            mydb_cursor.execute(INSERT_INTO_MYSQL, [a_square[0], a_square[1], b_square[0], b_square[1], d_crow, d_route])
            mydb.commit()
        except Exception as e:
            print("ERROR : inserting in db : " + str(e), file=sys.stderr)
            continue

print("Stopped at zipcode nb : " + str(counter))
