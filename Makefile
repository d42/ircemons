
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)
init:
	pip install -r requirements.txt

get_pokemans:
	bin/pokemon_scrapper
# XXX: switch to database much
clear_pokemans:
	find . -name "*.csv" -exec rm -v '{}' \;

db:
	bin/sync_db
