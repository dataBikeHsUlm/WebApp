#!/bin/env python3
from NominatimLibrary import Locator, NotFoundException
import psycopg2
import mysql.connector
import sys

# Nominatim postgreSQL
DB_NOMINATIM_NAME = "Planet"
DB_NOMINATIM_USER = "dataproject"
# TODO: ORDER BY performance ?
QUERY_POSTCODES_COUNTRIES = "SELECT DISTINCT country_code,postcode FROM location_area WHERE country_code IS NOT NULL AND postcode IS NOT NULL ORDER BY country_code, postcode;"

# MySQL
DB_MySQL_NAME = "geonom"
DB_MySQL_USER = "admin"
DB_MySQL_TABLE = "datamodel_zipcode"
INSERT_INTO_MYSQL = "INSERT INTO " + DB_MySQL_TABLE + " VALUES (%s, %s, %s, %s);"

DB_MySQL_PASSWORD = input("MySQL password : ")

print("Connecting to PostgreSQL database...")
postgres = psycopg2.connect('dbname=' + DB_NOMINATIM_NAME  + ' user=' + DB_NOMINATIM_USER)
pg_cursor = conn.cursor()

print("Connecting to MySQL database...")
mydb = mysql.connector.connect(
        host="localhost",
        user=DB_MySQL_USER,
        passwd=DB_MySQL_PASSWORD
)
mydb_cursor = mydb.cursor()

print("Executing query to get all postcodes per countries...")
pg_cursor.execute(QUERY_POSTCODES_COUNTRIES)

print("Executing query to get all postcodes per countries...")
counter = 0
while True:
    elm = pg_cursor.fetchone()
    if elm  == None:
        break
    else:
        country_code = elm[0].lower()
        zipcode = elm[1]

        print(counter + " : " + country_code + " : " + zipcode)

        # There already is a lon and lat in the file, use it ?
        try:
            # TODO: make more accurate queries ? (country name and city name)
            (lat, lon) = locator.get_coordinates("" + country_code + "," + zipcode)
        except NotFoundException:
            print("ERROR : " + query + " : not found, skipping...", file=sys.stderr)
            continue
        except Exception as e:
            print("ERROR : unknown error : " + e, file=sys.stderr)
            continue

        mysql.execute(INSERT_INTO_MYSQL, (counter, country_code, zipcode, 0, 0))
        counter += 1

print("Stopped at zipcode nb : " + counter)
postgres.close()
mydb.commit()
