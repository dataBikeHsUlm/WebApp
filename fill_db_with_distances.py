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
INSERT_INTO_MYSQL = "INSERT INTO " + DB_MySQL_TABLE_DIST + " VALUES (id, %s, %s, %s, %s, %s, %s, %s, %s);"

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
    coords = (city[3],city[4])
    res[coords] = True

keys = res.keys()
print("We are using " + str(len(keys)) + " instead of " + str((LON_MAX-LON_MIN)*(LAT_MAX-LAT_MIN)))
nb_paths = math.factorial(len(keys))/(math.factorial(2)*math.factorial(len(keys)-2))
print("This makes a total number of paths of : " + str(nb_paths))

print("Calculating distances between squares...")

# for (from_id, from_city) in enumerate(elms):
#     from_country_code = from_city[1]
#     from_zipcode = from_city[2]
#     from_coords = [from_city[3], from_city[4]]
# 
#     print("" + str(from_id) + " : " + str(from_country_code) + " : " + from_zipcode + " : " + str(from_coords))
# 
#     (mydb, mydb_cursor) = connect_mydb()
# 
#     for (to_id, to_city) in enumerate(elms):
#         counter += 1
# 
#         to_country_code = to_city[1]
#         to_zipcode = to_city[2]
#         to_coords = [to_city[3], to_city[4]]
# 
#         # print("" + str(to_id) + " : " + str(to_country_code) + " : " + to_zipcode + " : " + str(to_coords))
# 
#         d_crow = locator.distance_crow_coords(from_coords, to_coords);
# 
#         try:
#             d_route = locator.distance_route_coords(from_coords, to_coords);
#         except Exception as e:
#             print("ERROR : getting distance by route : " + str(e), file=sys.stderr)
#             if e.errno == 2055:
#                 (mydb, mydb_cursor) = connect_mydb()
#             continue
# 
#         try:
#             mydb_cursor.execute(INSERT_INTO_MYSQL, [d_crow, d_route, from_country_code, to_country_code, from_zipcode, to_zipcode, from_id + 1, to_id + 1])
#             mydb.commit()
#         except Exception as e:
#             print("ERROR : inserting in db : " + str(e), file=sys.stderr)
#             continue
# 
# print("Stopped at zipcode nb : " + str(counter))
