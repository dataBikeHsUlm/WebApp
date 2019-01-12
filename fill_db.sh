#!/bin/sh

TMP_FOLDER="$(pwd)/geonom/tmp"

# Creating tmp dir
if [ ! -d "tmp" ]
then
    rm -Rf $TMP_FOLDER
    mkdir -p $TMP_FOLDER
fi

sed "s/{{ COUNTRY_CODE }}/$COUNTRY_CODE/g" fill_db.py > $TMP_FOLDER/fill_db.py
ln -s tmp/NominatimLibrary geonom

cd $TMP_FOLDER

# Cloning NominatimLibrary
git clone http://github.com/dataBikeHsUlm/NominatimLibrary.git

python3 ../fill_db_from_osm.py

cd ..
rm -Rf $TMP_FOLDER
rm NominatimLibrary
