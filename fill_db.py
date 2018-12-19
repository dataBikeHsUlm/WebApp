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
    if len(c) < 4:
        print("ERROR : line too short : '" + ",".join(c) + "'", file=sys.stderr)
        continue

    country_code = c[0]
    zipcode = c[1]
    city = c[2]
    state = c[3]
    query = ",".join(c[:4])

    try:
        Zipcode.objects.get(country_iso = country_code, zip_code = zipcode)
    except Exception:
        print(country_code, zipcode)

        # There already is a lon and lat in the file, use it ?
        try:
            (lat, lon) = locator.get_coordinates(query)
        except NotFoundException:
            print("ERROR : " + query + " : not found, skipping...", file=sys.stderr)
            continue
        except Exception e:
            print("ERROR : unknown error : " + e, file=sys.stderr)
            continue

        Zipcode(country_iso = country_code, zip_code = zipcode, lat=lat, lon=lon).save()

