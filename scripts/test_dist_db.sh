#!/bin/sh

NB_TEST=$1

[ -n "$NB_TEST" ] || NB_TEST = 100

cd geonom
echo "from datamodel.models import *\ntest_distances_dbs(${NB_TEST})\n" | python3 manage.py shell
