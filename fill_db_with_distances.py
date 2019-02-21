#!/bin/env python3
from NominatimLibrary import Locator, NotFoundException
import psycopg2
import mysql.connector
import sys

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

print("Connecting to MySQL database...")
mydb = mysql.connector.connect(
        host="localhost",
        user=DB_MySQL_USER,
        passwd=DB_MySQL_PASSWORD,
        database=DB_MySQL_NAME
)
mydb_cursor = mydb.cursor()

print("Executing query to get all postcodes per countries...")
mydb_cursor.execute(QUERY_POSTCODES_COUNTRIES)
elms = mydb_cursor.fetchall()

print("Inserting postcodes in table...")
counter = 0

for (from_id, from_city) in enumerate(elms):
    from_country_code = from_city[0]
    from_zipcode = from_city[1]
    from_coords = [from_city[2], from_city[3]]

    print("" + str(from_id) + " : " + str(from_country_code) + " : " + from_zipcode + " : " + str(from_coords))

    for (to_id, to_city) in enumerate(elms[from_id+1:]):
        counter += 1

        to_country_code = to_city[0]
        to_zipcode = to_city[1]
        to_coords = [to_city[2], to_city[3]]

        # print("" + str(to_id) + " : " + str(to_country_code) + " : " + to_zipcode + " : " + str(to_coords))

        d_crow = locator.distance_crow_coords(from_coords, to_coords);
        d_route = locator.distance_route_coords(from_coords, to_coords);

        try:
            mydb_cursor.execute(INSERT_INTO_MYSQL, [d_crow, d_route, from_country_code, to_country_code, from_zipcode, to_zipcode, from_id + 1, from_id + to_id + 1])
            mydb.commit()
        except Exception as e:
            print("ERROR : inserting in db : " + str(e), file=sys.stderr)
            continue

print("Stopped at zipcode nb : " + str(counter))
