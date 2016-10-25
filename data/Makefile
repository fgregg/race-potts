include config.mk

nyc = 36 51000
la = 06 44000
chicago = 17 14000
houston = 48 35000
philadelphia = 42 60000
phoenix = 04 55000
san_antonio = 48 65000
san_diego = 06 66000
dallas = 48 19000
san_jose = 06 68000
austin = 48 05000
jacksonville = 12 35000
san_francisco = 06 67000
indianapolis = 18 36003 # Indianapolis city (balance)
columbus = 39 18000
fort_worth = 48 27000
charlotte = 37 12000
seattle = 53 63000
denver = 08 20000
el_paso = 48 24000
detroit = 26 22000
dc = 11 50000
boston = 25 07000
memphis = 47 48000
nashville = 47 52006 # Nashville-Davidson metropolitan government (balance)

%_tracts.geojson :
	python3 tracts.py $($*) > $@

%_blockgroups.geojson :
	python3 blockgroups.py $($*) > $@


%.shp : %.geojson
	ogr2ogr $@ $< -where "\"B03002_012E\" != '0' OR \"B03002_003E\" != '0' OR \"B03002_004E\" != '0'"


all :nyc_tracts.shp la_tracts.shp chicago_tracts.shp houston_tracts.shp philadelphia_tracts.shp phoenix_tracts.shp san_antonio_tracts.shp san_diego_tracts.shp dallas_tracts.shp san_jose_tracts.shp austin_tracts.shp jacksonville_tracts.shp san_francisco_tracts.shp indianapolis_tracts.shp columbus_tracts.shp fort_worth_tracts.shp charlotte_tracts.shp seattle_tracts.shp denver_tracts.shp el_paso_tracts.shp detroit_tracts.shp dc_tracts.shp boston_tracts.shp memphis_tracts.shp nashville_tracts.shp nyc_blockgroups.shp la_blockgroups.shp chicago_blockgroups.shp houston_blockgroups.shp philadelphia_blockgroups.shp phoenix_blockgroups.shp san_antonio_blockgroups.shp san_diego_blockgroups.shp dallas_blockgroups.shp san_jose_blockgroups.shp austin_blockgroups.shp jacksonville_blockgroups.shp san_francisco_blockgroups.shp indianapolis_blockgroups.shp columbus_blockgroups.shp fort_worth_blockgroups.shp charlotte_blockgroups.shp seattle_blockgroups.shp denver_blockgroups.shp el_paso_blockgroups.shp detroit_blockgroups.shp dc_blockgroups.shp boston_blockgroups.shp memphis_blockgroups.shp nashville_blockgroups.shp
