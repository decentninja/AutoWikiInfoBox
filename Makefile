test: birthyeartest


birthyeartest: data/birthyear.json data/birthYearHmmdata.json
	cat data/birthYear.json data/birthYearHmmdata.json | python2.7 searcher.py birthYear

data/birthyear.json:
	python2.7 birthYear 10000 > data/birthyear.json

data/birthYearHmmdata.json: data/birthyear.json
	cat data/birthYear.json | python2.7 parse.py birthYear date > data/birthYearHmmdata.json