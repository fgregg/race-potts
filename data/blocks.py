import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

from census_area import Census

from secrets import CENSUS_API_KEY

state_fips = sys.argv[1]
place_name = sys.argv[2]

c = Census(CENSUS_API_KEY)

fields = dict(hispanic_pop = 'P0040003',
              white_pop = 'P0050003',
              black_pop = 'P0050004')

place_geojson = c.sf1.state_place_block(tuple(fields.values()),
                                        state_fips, place_name,
                                        return_geometry=True,
                                        year=2010)

json.dump(place_geojson, sys.stdout)

