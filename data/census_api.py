import sys
import csv

from census import Census

import secrets

state, county, fields = sys.argv[1], sys.argv[2], sys.argv[3]

c = Census(secrets.CENSUS_API_KEY)
res = c.acs.state_county_blockgroup(['NAME'] + fields.split(','), 
                                    state, county, Census.ALL)

result_writer = csv.DictWriter(sys.stdout, res[0].keys()) 

result_writer.writeheader()
result_writer.writerows(res)



