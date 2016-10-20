import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

from census_area import Census

from secrets import CENSUS_API_KEY

state_fips = sys.argv[1]
place_name = sys.argv[2]

c = Census(CENSUS_API_KEY)

white_pop = 'P0050003'
black_pop = 'P0050004'
hispanic_pop = 'P0040003'

fields = (white_pop, black_pop, hispanic_pop)

place_geojson = c.state_place_block(fields, state_fips, place_name,
                                    return_geometry=True)

json.dump(place_geojson, sys.stdout)

