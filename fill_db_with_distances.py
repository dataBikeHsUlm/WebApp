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

for (id, from_city) in enumerate(elms):
    counter += 1
    from_country_code = from_city[0]
    from_zipcode = from_city[1]
    from_coords = [from_city[2], from_city[3]]

    print("" + str(id) + " : " + from_country_code + " : " + from_zipcode + " : " + str(from_coords))

#    # TODO: make more accurate queries with city name ?
#    query = country_name + " , " + zipcode
#    # There already is a lon and lat in the file, use it ?
#    try:
#        (lat, lon) = locator.get_coordinates(query)
#    except NotFoundException:
#        print("ERROR : " + query + " : not found, skipping...", file=sys.stderr)
#        continue
#    except Exception as e:
#        print("ERROR : unknown error : " + str(e), file=sys.stderr)
#        continue
#
#    try:
#        mydb_cursor.execute(INSERT_INTO_MYSQL, (counter, country_code, zipcode, lat, lon))
#        mydb.commit()
#    except Exception as e:
#        print("ERROR : inserting in db : `" + query + "` : " + str(e), file=sys.stderr)
#        continue

print("Stopped at zipcode nb : " + str(counter))
