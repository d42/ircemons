init:
	pip install -r requirements.txt


get_pokemans:
	./launch_scraper


# XXX: switch to database much
clear_pokemans:
	find . -name "*.csv" -exec rm -v '{}' \;
