include config.mk

cook_county_state_county = 17 031
la_county_state_county = 06 037
hennepin_county_state_county = 27 053 # minneapolis
harris_county_state_county = 48 201 # houston
new_york_county_state_county = 36 061
fulton_county_state_county = 13 121 # atlanta
maricopa_county_state_county = 04 013

NUMBERS := $(shell seq -w 2 78)
BLOCKGROUP_SHAPES := $(addsuffix .shapes,$(addprefix bg_,${NUMBERS}))

#.INTERMEDIATE : shapes bg_01.shapes block_group.table \
#	race.table la_race.csv shapes make_db

.PHONY : all drop_race

all : cook_county_race.shp la_county_race.shp hennepin_county_race.shp \
	harris_county_race.shp new_york_county_race.shp fulton_county_race.shp \
	maricopa_county_race.shp

%_race.shp : %_race.table shapes
	pgsql2shp -f $@ $(PG_DB) \
	"SELECT geoid, geom, \
	 \"B03002_001E\" as total, \"B03002_003E\" as non_hisp_white, \
	 \"B03002_004E\" as non_hisp_black, \"B03002_012E\" as hispanic \
	 FROM race, blockgroups \
	 WHERE statefp = state \
         AND countyfp = county \
         AND tractce::INT = tract \
         AND blkgrpce::INT = \"block group\" \
	 AND statefp = '$(word 1,$($*_state_county))' \
	 AND countyfp = '$(word 2,$($*_state_county))' \
	 AND \"B03002_001E\" > 0"	

## Tiger Shape Files

shapes : ${BLOCKGROUP_SHAPES}
	psql -d $(PG_DB) -c "ALTER TABLE blockgroups \
                             ALTER COLUMN geoid TYPE VARCHAR(19)"
	psql -d $(PG_DB) -c "UPDATE blockgroups SET geoid = '15000US' || geoid"
	touch shapes

bg_%.shapes : tl_2014_%_bg.* block_group.table
	- shp2pgsql -s 4326 -a $(basename $<).shp blockgroups | psql -d $(PG_DB)
	- touch $@

block_group.table bg_01.shapes : tl_2014_01_bg.* make_db
	shp2pgsql -I -s 4326 -d $(basename $<).shp blockgroups | psql -d $(PG_DB)
	touch block_group.table
	touch bg_01.shapes

tl_2014_%_bg.* : bg_%.zip
	- unzip $<
	- touch $@

bg_%.zip : 
	- wget -O $@ ftp://ftp2.census.gov/geo/tiger/TIGER2014/BG/tl_2014_$*_bg.zip

## Census Data

%_race.table : %_race.csv race.table
	cat $< | psql -d $(PG_DB) -c \
		"COPY $(basename $(word 2,$^)) FROM STDIN WITH CSV HEADER DELIMITER AS ','"
	touch $@

race.table : la_county_race.csv make_db
	csvsql --db "postgresql://$(PG_USER):$(PG_PASS)@$(PG_HOST):$(PG_PORT)/$(PG_DB)" \
		--tables $(basename $@) $<
	touch $@

%_race.csv : 
	python census_api.py $($*_state_county) B03002_001E,B03002_003E,B03002_004E,B03002_012E > $@

make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	touch $@

drop_race :
	psql -d $(PG_DB) -c "DROP TABLE IF EXISTS race"
	psql -d $(PG_DB) -c "DROP TABLE IF EXISTS blockgroups"
	- rm shapes
	- rm block_group.table
	- rm race.table
