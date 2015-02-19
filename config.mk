MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

PG_HOST="localhost"
PG_USER="fgregg"
PG_DB="race-potts"
PG_PORT="5432"
PG_PASS="buddah"
