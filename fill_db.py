import sys
from NominatimLibrary import Locator
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
    print(country_code, zipcode)

    # There already is a lon and lat in the file, use it ?
    (lat, lon) = locator.get_coordinates(country_code + "," + zipcode)

    # TODO: Check if code already exists ?
    try:
        Zipcode.objects.get(country_iso = country_code, zip_code = zipcode)
    except Exception:
        Zipcode(country_iso = country_code, zip_code = zipcode, lat=lat, lon=lon).save()

