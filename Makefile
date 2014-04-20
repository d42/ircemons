export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

init:
	pip install -r requirements.txt

debug:
	bin/pokemon_debug

pokemans:
	bin/pokemon_scraper

db:
	bin/sync_db
