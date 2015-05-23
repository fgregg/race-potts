include config.mk

la_county_state_county = 06 037
cook_county_state_county = 17 031
harris_county_state_county = 48 201 # houston
maricopa_county_state_county = 04 013 #phoenix
san_diego_county_state_county = 06 073
orange_county_state_county = 06 059
miami-date_county_state_county = 12 086
kings_county_state_county = 36 047
dallas_county_state_county = 48 113
riverside_county_state_county = 06 065
queens_county_state_county = 36 081
san_bernardino_county_state_county = 06 071
king_county_state_county = 53 033 # seattle
clark_county_state_county = 32 003 # las vegas
tarrant_county_state_county = 48 439 # fort worth
santa_clara_county_state_county = 06 085 # san jose
broward_county_state_county = 12 011 # fort lauderdale
bexar_county_state_county = 48 029 # san antonio
wayne_county_state_county = 26 163 # detroit
new_york_county_state_county = 36 061
philadelphia_county_state_county = 42 101
alameda_county_state_county = 06 001 # oakland
middlesex_county_state_county = 25 017 # boston
suffolk_county_state_county = 25 025
sacramento_county_state_county = 06 067
bronx_county_state_county = 36 005
nassau_county_state_county = 36 059
palm_beach_county_state_county = 12 099
cuyahoga_county_state_county = 39 035 # cleveland
hillsborough_county_state_county = 12 057 # tampa
allegheny_county_state_county = 42 003 # pittsburgh
oakland_county_state_county = 26 125 # detroit suburb
franklin_county_state_county = 39 049
orange_county_state_county = 12 095
hennepin_county_state_county = 27 053 # minneapolis
fairfax_county_state_county = 51 059
contra_costa_county_state_county = 06 013
travis_county_state_county = 48 453 # austin
salt_lake_county_state_county = 49 035 
st._louis_county_state_county = 29 189
montgomery_county_state_county = 24 031
pima_county_state_county = 04 019
honolulu_county_state_county = 15 003
westchester_county_state_county = 36 119
milwaukee_county_state_county = 55 079
fulton_county_state_county = 13 121 # atlanta
mecklenburg_county_state_county = 37 119 # charlotte, nc
fresno_county_state_county = 06 019
shelby_county_state_county = 47 157 # memphis
wake_county_state_county = 37 183 # wake

NUMBERS := $(shell seq -w 2 78)
BLOCKGROUP_SHAPES := $(addsuffix .shapes,$(addprefix bg_,${NUMBERS}))

#.INTERMEDIATE : shapes bg_01.shapes block_group.table \
#	race.table la_race.csv shapes make_db

.PHONY : all drop_race

all : la_county_race.shp cook_county_race.shp harris_county_race.shp	\
      maricopa_county_race.shp san_diego_county_race.shp		\
      orange_county_race.shp miami-date_county_race.shp			\
      kings_county_race.shp dallas_county_race.shp			\
      riverside_county_race.shp queens_county_race.shp			\
      san_bernardino_county_race.shp king_county_race.shp		\
      clark_county_race.shp tarrant_county_race.shp			\
      santa_clara_county_race.shp broward_county_race.shp		\
      bexar_county_race.shp wayne_county_race.shp			\
      new_york_county_race.shp philadelphia_county_race.shp		\
      alameda_county_race.shp middlesex_county_race.shp			\
      suffolk_county_race.shp sacramento_county_race.shp		\
      bronx_county_race.shp nassau_county_race.shp			\
      palm_beach_county_race.shp cuyahoga_county_race.shp		\
      hillsborough_county_race.shp allegheny_county_race.shp		\
      oakland_county_race.shp franklin_county_race.shp			\
      orange_county_race.shp hennepin_county_race.shp			\
      fairfax_county_race.shp contra_costa_county_race.shp		\
      travis_county_race.shp salt_lake_county_race.shp			\
      st._louis_county_race.shp montgomery_county_race.shp		\
      pima_county_race.shp honolulu_county_race.shp			\
      westchester_county_race.shp milwaukee_county_race.shp		\
      fulton_county_race.shp mecklenburg_county_race.shp		\
      fresno_county_race.shp shelby_county_race.shp			\
      wake_county_race.shp

%_race.shp : %_race.table shapes
	pgsql2shp -f $@ $(PG_DB) \
	"SELECT geoid, geom, \
	 \"B03002_001E\" as total, \"B03002_003E\" as non_hisp_white, \
	 \"B03002_004E\" as non_hisp_black, \"B03002_012E\" as hispanic \
	 FROM race, blockgroups \
	 WHERE statefp = state \
         AND countyfp = county \
         AND tractce::INT = tract::INT \
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

.PRECIOUS : %_race.table
%_race.table : %_race.csv race.table
	cat $< | psql -d $(PG_DB) -c \
		"COPY $(basename $(word 2,$^)) FROM STDIN WITH CSV HEADER DELIMITER AS ','"
	touch $@

race.table : san_bernardino_county_race.csv make_db
	csvsql --db "postgresql://$(PG_USER):$(PG_PASS)@$(PG_HOST):$(PG_PORT)/$(PG_DB)" \
		--tables $(basename $@) $<
	psql -d $(PG_DB) -c "ALTER TABLE race ADD CONSTRAINT unique_name UNIQUE(\"NAME\")"

	touch $@

%_race.csv : 
	python census_api.py $($*_state_county) B03002_001E,B03002_003E,B03002_004E,B03002_012E > $@

make_db :
	createdb $(PG_DB)
	psql -d $(PG_DB) -c "CREATE EXTENSION postgis"
	touch $@

drop_race :
	psql -d $(PG_DB) -c "DROP TABLE IF EXISTS race"
	- rm shapes
	- rm block_group.table
	- rm race.table
	- rm *_race.table

