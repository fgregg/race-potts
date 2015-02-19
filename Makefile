include config.mk


tl_2014_us_tbg.zip :
	wget -O $@ "ftp://ftp2.census.gov/geo/tiger/TIGER2014/TBG/tl_2014_us_tbg.zip"

tl_2014_us_tbg.shp : tl_2014_us_tbg.zip
	unzip $<
	touch $@

make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	touch make_db

blocks.table : tl_2014_us_tbg.shp make_db
	shp2pgsql -I -s 4326 -d $< $(basename $@) | psql -d $(PG_DB)

chicago_race.zip :  
	wget -O $@ "http://api.censusreporter.org/1.0/data/download/latest?table_ids=B02001&geo_ids=16000US1714000,150|16000US1714000&format=csv"

chicago_race.csv : chicago_race.zip
	unzip -c $< | sed -n '/geoid/,$$p' > t1.csv
	(grep 'geoid' t1.csv | python collapse_headers.py; \
	 tail -n +2 t1.csv) | grep -v ^$$ > t2.csv
	csvclean t2.csv
	mv t2_out.csv $@
	rm t1.csv t2.csv

chicago_race.table : chicago_race.csv
	csvsql --db "postgresql://$(PG_USER)@$(PG_HOST):$(PG_PORT)/$(PG_DB)" \
		--tables $(basename $<) $<
	cat $< | psql -U $(PG_USER) -h $(PG_HOST) -p $(PG_PORT) -d $(PG_DB) -c \
		"COPY $(basename $@) FROM STDIN WITH CSV HEADER DELIMITER ','"
	touch $@



all : blocks.table


