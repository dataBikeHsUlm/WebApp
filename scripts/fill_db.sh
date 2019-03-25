#!/bin/sh

pip3 install mysql-connector psycopg2

# Cloning NominatimLibrary
rm -Rf NominatimLibrary
git clone http://github.com/dataBikeHsUlm/NominatimLibrary.git

# python3 fill_db_from_osm.py
python3 fill_db_with_distances.py

rm -Rf NominatimLibrary
