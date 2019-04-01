#!/bin/env python3
from NominatimLibrary import Locator, NotFoundException
import psycopg2
import mysql.connector
import sys

POSTCODE_FILE="scripts/geoname_postcodes_world.txt"

# Nominatim postgreSQL
# DB_NOMINATIM_NAME = "Planet"
DB_NOMINATIM_NAME = "Europe"
DB_NOMINATIM_USER = "dataproject"
# TODO: ORDER BY performance ?
QUERY_POSTCODES_COUNTRIES = "SELECT DISTINCT location_area.country_code,postcode,country_name.name FROM (location_area LEFT JOIN country_name ON location_area.country_code = country_name.country_code) WHERE location_area.country_code IS NOT NULL AND postcode IS NOT NULL ORDER BY country_code, postcode;"

# MySQL
DB_MySQL_NAME = "geonom"
DB_MySQL_USER = "admin"
DB_MySQL_TABLE = "datamodel_zipcode"
GET_ALL_EXISTING = "SELECT country_iso,zip_code FROM " + DB_MySQL_TABLE + ";"
INSERT_INTO_MYSQL = "INSERT INTO " + DB_MySQL_TABLE + " VALUES (%s, %s, %s, %s, %s);"

print(" --------------------------------- ")
DB_MySQL_PASSWORD = input("MySQL password : ")

locator = Locator(use_fallback = True)

print("Connecting to PostgreSQL database...")
postgres = psycopg2.connect('dbname=' + DB_NOMINATIM_NAME  + ' user=' + DB_NOMINATIM_USER)
pg_cursor = postgres.cursor()

print("Connecting to MySQL database...")
mydb = mysql.connector.connect(
        host="localhost",
        user=DB_MySQL_USER,
        passwd=DB_MySQL_PASSWORD,
        database=DB_MySQL_NAME
)
mydb_cursor = mydb.cursor()

print("Executing query to get all postcodes per countries...")
pg_cursor.execute(QUERY_POSTCODES_COUNTRIES)

print("Getting all existing cities...")
mydb_cursor.execute(GET_ALL_EXISTING)
elms = mydb_cursor.fetchall()
existing = {}
for [country_iso,zip_code] in elms:
    existing[(country_iso,zip_code)] = True

print("Inserting postcodes in table...")
counter = 0
errors = 0
errors_list = []
countries = {}
while True:
    elm = pg_cursor.fetchone()
    if elm  == None:
        break
    else:
        counter += 1
        country_code = elm[0].upper()
        zipcode = elm[1]

        countries[country_code] = True

        # Works better with english name :
        index = elm[2].find("\"name:en")

        # But, it might not be found, if so use the default name :
        if index < 0:
            index = 0
        country_name = elm[2][index:].split('"')[3]

        if existing.get((country_code,zipcode)) != True:
            print("" + str(counter) + " : " + country_code + " : " + country_name + " : " + zipcode)

            # TODO: make more accurate queries with city name ?
            query = country_name + " , " + zipcode
            # There already is a lon and lat in the file, use it ?
            try:
                (lat, lon) = locator.get_coordinates(query)
            except NotFoundException:
                print("ERROR : " + query + " : not found, skipping...", file=sys.stderr)
                errors_list.append((country_code,zipcode,country_name))
                errors += 1
                continue
            except Exception as e:
                print("ERROR : unknown error : " + str(e), file=sys.stderr)
                errors_list.append((country_code,zipcode,country_name))
                errors += 1
                continue

            try:
                mydb_cursor.execute(INSERT_INTO_MYSQL, (counter, country_code, zipcode, lat, lon))
                mydb.commit()
            except Exception as e:
                print("ERROR : inserting in db : `" + query + "` : " + str(e), file=sys.stderr)
                errors_list.append((country_code,zipcode,country_name))
                errors += 1
                continue
            existing[(country_code,zipcode)] = True

with open(POSTCODE_FILE) as f:
    while True:
        line = f.readline()
        if len(line) == 0:
            break

        cols = line.split("\t")
        country_code,zipcode,_,_,_,_,_,_,_,lat,lon,_ = cols

        # In case of Luxembourg, the postcodes begin with a 'L-' while in Nominatim they don't...
        if country_code == "LE":
            zipcode = zipcode[2:]

        if countries.get(country_code) == True and existing.get((country_code,zipcode)) != True:
            counter += 1
            print("" + str(counter) + " : " + country_code + " : " + zipcode)

            try:
                mydb_cursor.execute(INSERT_INTO_MYSQL, (counter, country_code, zipcode, lat, lon))
                mydb.commit()
            except Exception as e:
                print("ERROR : inserting in db : `" + query + "` : " + str(e), file=sys.stderr)
                errors_list.append((country_code,zipcode,country_name))
                errors += 1
                continue
            existing[(country_code,zipcode)] = True

print("Stopped at zipcode nb : " + str(counter))
print(str(errors) + " errors occurred")
postgres.close()

with open("res.csv",mode="w") as f:
    f.write("%s,%s,%s\n" % ("country_iso","postcode","country_name"))
    for e in errors_list:
        f.write("%s,%s,%s\n" % e)
