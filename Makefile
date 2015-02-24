include config.mk

chicago_fips = 16000US1714000
nyc_fips = 16000US3651000
atlanta_fips = 16000US1304000
houston_fips = 16000US4835000
la_fips = 16000US0644000

NUMBERS := $(shell seq -w 2 78)
BLOCKGROUP_SHAPES := $(addsuffix .shapes,$(addprefix bg_,${NUMBERS}))

shapes : ${BLOCKGROUP_SHAPES}
	psql -d $(PG_DB) -c "ALTER TABLE blockgroups \
                             ALTER COLUMN geoid TYPE VARCHAR(19)"
	psql -d $(PG_DB) -c "UPDATE blockgroups SET geoid = '15000US' || geoid"
	rm *.shapes
	touch shapes


bg_%.zip : 
	- wget -O $@ ftp://ftp2.census.gov/geo/tiger/TIGER2014/BG/tl_2014_$*_bg.zip

tl_2014_%_bg.* : bg_%.zip
	- unzip $<
	- touch $@

bg_%.shapes : tl_2014_%_bg.* block_group.table
	- shp2pgsql -s 4326 -a $(basename $<).shp blockgroups | psql -d $(PG_DB)
	- touch $@

block_group.table bg_01.shapes : tl_2014_01_bg.*
	shp2pgsql -I -s 4326 -d $(basename $<).shp blockgroups | psql -d $(PG_DB)
	touch block_group.table
	touch bg_01.shapes

make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	touch make_db

blocks.table : tl_2014_us_tbg.shp make_db
	shp2pgsql -s 4326 -d $< $(basename $@) | psql -d $(PG_DB)
	touch blocks.table

%_race.zip : 
	wget -O $@ "http://api.censusreporter.org/1.0/data/download/latest?table_ids=B02001&geo_ids=$($*_fips),150|$($*_fips)&format=csv"


%_race.csv : %_race.zip
	unzip -c $< | sed -n '/geoid/,$$p' | sed -n '/inflating/q;p' > temp_$@
	(grep 'geoid' temp_$@ | python collapse_headers.py; \
	 tail -n +2 temp_$@) | grep -v ^$$ > $@
	rm temp_$@

race.table : 
	csvsql --db "postgresql://$(PG_USER)@$(PG_HOST):$(PG_PORT)/$(PG_DB)" \
		--tables $(basename $@) typical_race.csv
	touch $@

%_race.table : %_race.csv race.table
	cat $< | psql -U $(PG_USER) -h $(PG_HOST) -p $(PG_PORT) -d $(PG_DB) -c \
		"COPY $(basename $(word 2,$^)) FROM STDIN WITH CSV HEADER DELIMITER AS ','"
	touch $@

all : chicago_race.table nyc_race.table atlanta_race.table \
	la_race.table

clean : 
	rm tl_2014_us_tbg.*

