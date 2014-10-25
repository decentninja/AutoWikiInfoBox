# Default property
# Can be changed with "make test property=parent type=link" for example
# More properties can be found at http://dbpedia.org/ontology/Person
property = birthYear
type = date
ns = dbo

test: data/$(property).json data/$(property)Hmmdata.json viterbi
	cat data/$(property).json data/$(property)Hmmdata.json | python2.7 searcher.py $(property) $(type)

data/$(property).json:
	python2.7 query.py $(ns):$(property) 10000 > data/$(property).json

data/$(property)Hmmdata.json: data/$(property).json
	cat data/$(property).json | python2.7 parse.py $(property) $(type) > data/$(property)Hmmdata.json

clean:
	rm data/*Hmmdata.json
	rm viterbi
	rm *.pyc

cleanall:
	rm data/*
	rm viterbi
	rm *.pyc

viterbi: anotherhmmthing/viterbi.cpp
	g++ anotherhmmthing/viterbi.cpp -Wall -std=c++11 -g -o viterbi
