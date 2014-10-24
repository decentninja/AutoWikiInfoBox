test: birthyeartest


birthyeartest: data/birthyear.json data/birthYearHmmdata.json
	cat data/birthYear.json data/birthYearHmmdata.json | python2.7 searcher.py birthYear

data/birthyear.json:
	python2.7 query.py birthYear 1000 > data/birthyear.json

data/birthYearHmmdata.json: data/birthyear.json
	cat data/birthYear.json | python2.7 parse.py birthYear date > data/birthYearHmmdata.json

clean:
	rm data/*