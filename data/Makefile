MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

PG_DB = race_potts
CHECK_RELATION = psql -d $(PG_DB) -c "\d $@" > /dev/null 2>&1

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

.PRECIOUS : %_blocks.geojson %_2011_blockgroups.geojson

$(PG_DB) :
	createdb $@
	psql -d $@ -c "CREATE EXTENSION POSTGIS"

%_2011_blockgroups.geojson :
	python3 blockgroups.py $($*) 2011 > $@

%_blocks.geojson :
	python3 blocks.py $($*) > $@

.PHONY : %_blocks %_2011_blockgroups
%_blocks : %_blocks.geojson
	$(CHECK_RELATION) || \
	ogr2ogr -f "PostgreSQL" PG:"dbname=$(PG_DB)" $< -nln $@ -nlt MULTIPOLYGON

%_2011_blockgroups : %_2011_blockgroups.geojson
	$(CHECK_RELATION) || \
	ogr2ogr -f "PostgreSQL" PG:"dbname=$(PG_DB)" $< -nln $@ -nlt MULTIPOLYGON


%_blocks.shp : %_blocks %_2011_blockgroups
	ogr2ogr -f "ESRI Shapefile" $@ PG:"dbname=$(PG_DB)" -sql \
	    "SELECT p0050003::INT, p0050004::INT, p0040003::INT, $<.wkb_geometry, \
                    SUM(blockgroups.b25064_001e * \
                        ST_Area(ST_Intersection(blockgroups.wkb_geometry, \
                                                $<.wkb_geometry))) / \
                    ST_Area($<.wkb_geometry) AS b25064_001e \
             FROM (SELECT ogc_fid, original.wkb_geometry, \
                   COALESCE(original.b25064_001e::FLOAT, \
                            touching.b25064_001e, \
                            knn.b25064_001e) AS b25064_001e \
                   FROM $(word 2,$^) AS original \
                   LEFT JOIN \
                        (SELECT a.ogc_fid, AVG(b.b25064_001e::FLOAT) AS b25064_001e \
                         FROM $(word 2,$^) AS a \
                         LEFT JOIN $(word 2,$^) AS b \
                             ON ST_Touches(a.wkb_geometry, b.wkb_geometry) \
                                AND a.ogc_fid != b.ogc_fid \
                         WHERE b.b25064_001e IS NOT NULL \
                         GROUP BY a.ogc_fid) AS touching \
                       USING (ogc_fid) \
                   INNER JOIN \
                        (WITH subq AS (SELECT a.ogc_fid, \
                                              UNNEST(ARRAY(SELECT b.b25064_001e::FLOAT \
                                                           FROM $(word 2,$^) AS b \
                                                           WHERE a.ogc_fid != b.ogc_fid \
                                                               AND b.b25064_001e IS NOT NULL \
                                                           ORDER BY a.wkb_geometry <#> b.wkb_geometry \
                                                           LIMIT 5)) AS neighbors \
                                       FROM $(word 2,$^) AS a) \
                         SELECT ogc_fid, AVG(neighbors) AS b25064_001e \
                         FROM subq \
                         GROUP BY ogc_fid) AS knn \
                       USING (ogc_fid)) AS blockgroups \
             INNER JOIN $< \
                 ON ST_Intersects(blockgroups.wkb_geometry, $<.wkb_geometry) \
             WHERE p0050003 != '0' OR p0050004 != '0' OR p0040003 != '0' \
             GROUP BY $<.ogc_fid \
             HAVING SUM(ST_Area(ST_Intersection(blockgroups.wkb_geometry, \
                    		                            $<.wkb_geometry))) / \
                        ST_Area($<.wkb_geometry) > 0.9"



.PHONY : blocks
blocks : nyc_blocks.shp la_blocks.shp chicago_blocks.shp houston_blocks.shp philadelphia_blocks.shp phoenix_blocks.shp san_antonio_blocks.shp san_diego_blocks.shp dallas_blocks.shp san_jose_blocks.shp austin_blocks.shp jacksonville_blocks.shp san_francisco_blocks.shp indianapolis_blocks.shp columbus_blocks.shp fort_worth_blocks.shp charlotte_blocks.shp seattle_blocks.shp denver_blocks.shp el_paso_blocks.shp detroit_blocks.shp dc_blocks.shp boston_blocks.shp memphis_blocks.shp nashville_blocks.shp

all : blocks
