#!/bin/sh

# Codes from : http://download.geonames.org/export/zip/

# It is a country code of two letters (i.e. `DE`) or `allCountries` for all of them.
COUNTRY_CODE="$1"

ZIPCODES_SOURCE="http://download.geonames.org/export/zip"
TMP_FOLDER="$(pwd)/geonom/tmp"

ARCHIVE_NAME="${COUNTRY_CODE}.zip"

if [ ! -n "$COUNTRY_CODE" ]
then
    echo "Please provide a country code as parameter." 2>&1
    exit 1
fi

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

# Get zipcodes for the requested country code :
wget "$ZIPCODES_SOURCE/$ARCHIVE_NAME"

unzip "$ARCHIVE_NAME"

cat fill_db.py | python3 ../manage.py shell

cd ..
rm -Rf $TMP_FOLDER
rm NominatimLibrary
