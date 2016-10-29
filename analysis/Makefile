all : emergence.pdf

params_%.csv :
	python3 $*.py > $@

emergence.pdf : emergence.Rnw params_blocks.csv
	echo 'library(knitr); knit2pdf("$<")' | R --no-save
