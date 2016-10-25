import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

from census_area import Census

from secrets import CENSUS_API_KEY

state_fips = sys.argv[1]
place_name = sys.argv[2]

c = Census(CENSUS_API_KEY)

fields = dict(hispanic_pop = 'B03002_012E',
              white_pop = 'B03002_003E',
              black_pop = 'B03002_004E',
              median_monthly_housting_cost = 'B25105_001E')

place_geojson = c.acs5.state_place_tract(tuple(fields.values()),
                                         state_fips, place_name,
                                         return_geometry=True)

json.dump(place_geojson, sys.stdout)

