#!/bin/sh

pip3 install --user mysql-connector psycopg2

if pwd | grep "scripts$" > /dev/null
then
    cd ..
fi

# Cloning NominatimLibrary
if [ ! -d scripts/NominatimLibrary ]
then
    git clone http://github.com/dataBikeHsUlm/NominatimLibrary.git scripts/NominatimLibrary
fi

python3 fill_db_postcodes.py
python3 fill_db_with_distances.py
