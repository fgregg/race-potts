include config.mk

nyc = 36 "New York city"
la = 06 "Los Angeles city"
chicago = 17 "Chicago city"
houston = 48 "Houston city"
philadelphia = 42 "Philadelphia city"
phoenix = 04 "Phoenix city"
san_antonio = 48 "San Antonio city"
san_diego = 06 "San Diego city"
dallas = 48 "Dallas city"
san_jose = 06 "San Jose city"
austin = 48 "Austin city"
jacksonville = 12 "Jacksonville city"
san_francisco = 06 "San Francisco city"
indianapolis = 18 "Indianapolis city"
columbus = 39 "Columbus city"
fort_worth = 48 "Fort Worth city"
charlotte = 37 "Charlotte city"
seattle = 53 "Seattle city"
denver = 08 "Denver city"
el_paso = 48 "El Paso city"
detroit = 26 "Detroit city"
dc = 11 "Washington city"
boston = 25 "Boston city"
memphis = 47 "Memphis city"
nashville = 47 "Nashville-Davidson metropolitan government (balance)"

.PRECIOUS : nyc.geojson la.geojson chicago.geojson houston.geojson philadelphia.geojson phoenix.geojson san_antonio.geojson san_diego.geojson dallas.geojson san_jose.geojson austin.geojson jacksonville.geojson san_francisco.geojson indianapolis.geojson columbus.geojson fort_worth.geojson charlotte.geojson seattle.geojson denver.geojson el_paso.geojson detroit.geojson dc.geojson boston.geojson memphis.geojson nashville.geojson
%.geojson :
	python3 census_place.py $($*) > $@

%.shp : %.geojson
	ogr2ogr $@ $< -where "\"B03002_012E\" != '0' OR \"B03002_003E\" != '0' OR \"B03002_004E\" != '0'"


all : nyc.shp la.shp chicago.shp san_diego.shp dallas.shp austin.shp jacksonville.shp san_francisco.shp columbus.shp charlotte.shp seattle.shp denver.shp el_paso.shp detroit.shp dc.shp boston.shp memphis.shp nashville.shp phoenix.shp philadelphia.shp 

rest : san_jose.shp indianapolis.shp fort_worth.shp houston.shp san_antonio.shp
