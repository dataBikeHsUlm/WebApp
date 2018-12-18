import sys
from NominatimLibrary import Locator, NotFoundException
from datamodel.models import Zipcode

COUNTRY_CODE="{{ COUNTRY_CODE }}"

codes_filename = COUNTRY_CODE + ".txt"
locator = Locator()

print("Reading from :", codes_filename)
with open(codes_filename, 'r') as file:
    lines = [l.split("\t") for l in file.read().split("\n")]

print("Parsing lines...")
for c in lines:
    country_code = c[0]
    zipcode = c[1]

    try:
        Zipcode.objects.get(country_iso = country_code, zip_code = zipcode)
    except Exception:
        print(country_code, zipcode)

        # There already is a lon and lat in the file, use it ?
        try:
            (lat, lon) = locator.get_coordinates(country_code + "," + zipcode)
        except NotFoundException:
            print("ERROR : " + country_code + ", " + zipcode + " : not found, skipping...")
            continue

        Zipcode(country_iso = country_code, zip_code = zipcode, lat=lat, lon=lon).save()

