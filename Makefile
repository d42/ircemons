init:
	pip install -r requirements.txt


get_pokemans:
	./launch_scrapper


# XXX: switch to database much
clear_pokemans:
	find . -name "*.csv" -exec rm -v '{}' \;
