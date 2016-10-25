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

%_2014_blockgroups.geojson :
	python3 blockgroups.py $($*) 2014 > $@

%_2011_blockgroups.geojson :
	python3 blockgroups.py $($*) 2011 > $@

%_blocks.geojson :
	python3 blocks.py $($*) > $@

%_tracts.shp : %_tracts.geojson
	ogr2ogr $@ $< -where "(\"B03002_012E\" != '0' OR \
                               \"B03002_003E\" != '0' OR \
                               \"B03002_004E\" != '0') AND \
                               \"B25105_001E\" IS NOT NULL"

%_blockgroups.shp : %_blockgroups.geojson
	ogr2ogr $@ $< -where "(\"B03002_012E\" != '0' OR \
                               \"B03002_003E\" != '0' OR \
                               \"B03002_004E\" != '0')"

%_blocks.shp : %_blocks.geojson
	ogr2ogr $@ $< -where "(\"P0050003\" != '0' OR \
                               \"P0050004\" != '0' OR \
                               \"P0040003\" != '0')"


.PHONY : 2014_blockgroups
2014_blockgroups : nyc_2014_blockgroups.shp la_2014_blockgroups.shp chicago_2014_blockgroups.shp houston_2014_blockgroups.shp philadelphia_2014_blockgroups.shp phoenix_2014_blockgroups.shp san_antonio_2014_blockgroups.shp san_diego_2014_blockgroups.shp dallas_2014_blockgroups.shp san_jose_2014_blockgroups.shp austin_2014_blockgroups.shp jacksonville_2014_blockgroups.shp san_francisco_2014_blockgroups.shp indianapolis_2014_blockgroups.shp columbus_2014_blockgroups.shp fort_worth_2014_blockgroups.shp charlotte_2014_blockgroups.shp seattle_2014_blockgroups.shp denver_2014_blockgroups.shp el_paso_2014_blockgroups.shp detroit_2014_blockgroups.shp dc_2014_blockgroups.shp boston_2014_blockgroups.shp memphis_2014_blockgroups.shp nashville_2014_blockgroups.shp

.PHONY 2011_blockgroups
2011_blockgroups : nyc_2011_blockgroups.shp la_2011_blockgroups.shp chicago_2011_blockgroups.shp houston_2011_blockgroups.shp philadelphia_2011_blockgroups.shp phoenix_2011_blockgroups.shp san_antonio_2011_blockgroups.shp san_diego_2011_blockgroups.shp dallas_2011_blockgroups.shp san_jose_2011_blockgroups.shp austin_2011_blockgroups.shp jacksonville_2011_blockgroups.shp san_francisco_2011_blockgroups.shp indianapolis_2011_blockgroups.shp columbus_2011_blockgroups.shp fort_worth_2011_blockgroups.shp charlotte_2011_blockgroups.shp seattle_2011_blockgroups.shp denver_2011_blockgroups.shp el_paso_2011_blockgroups.shp detroit_2011_blockgroups.shp dc_2011_blockgroups.shp boston_2011_blockgroups.shp memphis_2011_blockgroups.shp nashville_2011_blockgroups.shp


.PHONY : blocks
blocks : nyc_blocks.shp la_blocks.shp chicago_blocks.shp houston_blocks.shp philadelphia_blocks.shp phoenix_blocks.shp san_antonio_blocks.shp san_diego_blocks.shp dallas_blocks.shp san_jose_blocks.shp austin_blocks.shp jacksonville_blocks.shp san_francisco_blocks.shp indianapolis_blocks.shp columbus_blocks.shp fort_worth_blocks.shp charlotte_blocks.shp seattle_blocks.shp denver_blocks.shp el_paso_blocks.shp detroit_blocks.shp dc_blocks.shp boston_blocks.shp memphis_blocks.shp nashville_blocks.shp


all : 2014_blockgroups 2011_blockgroups blocks
