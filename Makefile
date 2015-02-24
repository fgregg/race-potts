include config.mk

chicago_fips = 16000US1714000
nyc_fips = 16000US3651000
atlanta_fips = 16000US1304000
houston_fips = 16000US4835000
la_fips = 16000US0644000

NUMBERS := $(shell seq -w 2 78)
BLOCKGROUP_SHAPES := $(addsuffix .shapes,$(addprefix bg_,${NUMBERS}))

.INTERMEDIATE : shapes bg_01.shapes block_group.table \
	race.table la_race.csv

.PHONY : all
all : chicago_race.shp nyc_race.shp atlanta_race.shp la_race.shp

%_race.shp : %_race.table shapes
	pgsql2shp -f $@ -h $(PG_HOST) -u $(PG_USER) -p $(PG_PORT) $(PG_DB) \
	"SELECT geoid, geom, \
	 \"B03002001\" as total, \"B03002003\" as non_hisp_white, \
	 \"B03002004\" as non_hisp_black, \"B03002012\" as hispanic \
	 FROM race INNER JOIN blockgroups USING (geoid) \
	 WHERE placefips = '$($*_fips)'"	

## Tiger Shape Files

shapes : ${BLOCKGROUP_SHAPES}
	psql -d $(PG_DB) -c "ALTER TABLE blockgroups \
                             ALTER COLUMN geoid TYPE VARCHAR(19)"
	psql -d $(PG_DB) -c "UPDATE blockgroups SET geoid = '15000US' || geoid"
	rm *.shapes
	touch shapes

bg_%.shapes : tl_2014_%_bg.* block_group.table
	- shp2pgsql -s 4326 -a $(basename $<).shp blockgroups | psql -d $(PG_DB)
	- touch $@

block_group.table bg_01.shapes : tl_2014_01_bg.*
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
	cat $< | psql -U $(PG_USER) -h $(PG_HOST) -p $(PG_PORT) -d $(PG_DB) -c \
		"COPY $(basename $(word 2,$^)) FROM STDIN WITH CSV HEADER DELIMITER AS ','"
	touch $@

race.table : la_race.csv 
	csvsql --db "postgresql://$(PG_USER)@$(PG_HOST):$(PG_PORT)/$(PG_DB)" \
		--tables $(basename $@) $<
	touch $@

%_race.csv : %_race.zip
	unzip -c $< | sed -n '/geoid/,$$p' | sed -n '/inflating/q;p' > temp_$@
	(grep 'geoid' temp_$@ | python collapse_headers.py | \
	 sed 's/$$/,placefips/'; \
	 tail -n +2 temp_$@ ) | grep -v ^$$ | \
	 sed '2,$$s/$$/,$($*_fips)/' > $@
	rm temp_$@

%_race.zip : 
	wget -O $@ "http://api.censusreporter.org/1.0/data/download/latest?table_ids=B03002&geo_ids=$($*_fips),150|$($*_fips)&format=csv"


make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	touch make_db

drop_race :
	psql -d $(PG_DB) -c "DROP TABLE IF EXISTS race"
	rm *_race.table
	rm race.table
