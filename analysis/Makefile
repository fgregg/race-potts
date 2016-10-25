all : params_blocks.csv params_blockgroups.csv params_tracts.csv

params_blocks.csv :
	python3 blocks.py > $@

params_blockgroups.csv :
	python3 blockgroups.py > $@

params_tracts.csv :
	python3 tracts.py > $@

