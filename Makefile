include config.mk

chicago_fips = 16000US1714000
nyc_fips = 16000US3651000
atlanta_fips = 16000US1304000
houston_fips = 16000US4835000
la_fips = 16000US0644000
dc_fips = 16000US1150000
minneapolis_fips = 16000US2743000



make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	psql -d $(PG_DB) -c "CREATE ROLE census"

%_backup.sql.gz : 
	wget "https://s3.amazonaws.com/census-backup/acs/2013/$*/$*_backup.sql.gz"
	touch $@

%.table : %_backup.sql.gz
	pv $< | gunzip |  sed 's/^\(.*COMMENT .*\)/-- \1/g' | psql -q 	-d $(PG_DB)
	touch $@

all.tables : acs2013_5yr.table tiger2012.table
	touch $@

%_race.shp : all.tables
	pgsql2shp -f $@ -h $(PG_HOST) -u $(PG_USER) -p $(PG_PORT) $(PG_DB) \
	"SELECT geoid, geom, \
	 \"B03002001\" as total, \"B03002003\" as non_hisp_white, \
	 \"B03002004\" as non_hisp_black, \"B03002012\" as hispanic \
	 FROM race INNER JOIN blockgroups USING (geoid) \
	 WHERE placefips = '$($*_fips)'"	

all : chicago_race.shp nyc_race.shp atlanta_race.shp la_race.shp \
	houston_race.shp dc_race.shp minneapolis_race.shp
 


