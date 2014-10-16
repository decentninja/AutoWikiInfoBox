import json
import urllib2
import sys

def warning(str):
	sys.stderr.write("\033[91m" + str + "\n\033[95m")

if len(sys.argv) == 2:
	warning("""
use: python main.py [field] [item type] [item limit] [characters around key]
example: python main.py birthDate date 100
Check http://dbpedia.org/ontology/Person for more fields.
	""")
	sys.exit(1)

property = sys.argv[1]
type = sys.argv[2]
limit = 100
if len(sys.argv) >= 4:
	limit = sys.argv[3]
AROUND = 36
if len(sys.argv) >= 5:
	AROUND = int(sys.argv[4])
# Go to this link to modify the query:
# http://dbpedia.org/snorql/?query=PREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Fname+%3FbirthName+%28group_concat%28%3Fbirth%3Bseparator%3D%27%3B%27%29+as+%3Fbirth%29+%28group_concat%28%3Fdeath%3Bseparator%3D%27%3B%27%29+as+%3Fdeath%29+%28group_concat%28%3FknownFor%3Bseparator%3D%27%3B%27%29+as+%3FknownFor%29+%3Fperson+%3Fdescription_en+WHERE+%7B%0D%0A+++++%3Fperson+dbo%3AbirthDate+%3Fbirth+.%0D%0A+++++%3Fperson+dbo%3AbirthName+%3FbirthName+.%0D%0A+++++%3Fperson+foaf%3Aname+%3Fname+.%0D%0A+++++%3Fperson+dbo%3AdeathDate+%3Fdeath+.%0D%0A+++++%3Fperson+rdfs%3Acomment+%3Fdescription_en+.%0D%0A+++++%3Fperson+dbo%3AknownFor+%3FknownFor+.%0D%0A+++++FILTER+%28LANG%28%3Fdescription_en%29+%3D+%27en%27%29+.%0D%0A%7D%0D%0Agroup+by+%3Fname+%3Fdescription_en+%3Fperson+%3FbirthName%0D%0AORDER+BY+%3Fname%0D%0ALIMIT+100
predefined = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Fname+%3FbirthName+%28group_concat%28%3Fbirth%3Bseparator%3D%27%3B%27%29+as+%3Fbirth%29+%28group_concat%28%3Fdeath%3Bseparator%3D%27%3B%27%29+as+%3Fdeath%29+%28group_concat%28%3FknownFor%3Bseparator%3D%27%3B%27%29+as+%3FknownFor%29+%3Fperson+%3Fdescription_en+WHERE+%7B%0D%0A+++++%3Fperson+dbo%3AbirthDate+%3Fbirth+.%0D%0A+++++%3Fperson+dbo%3AbirthName+%3FbirthName+.%0D%0A+++++%3Fperson+foaf%3Aname+%3Fname+.%0D%0A+++++%3Fperson+dbo%3AdeathDate+%3Fdeath+.%0D%0A+++++%3Fperson+rdfs%3Acomment+%3Fdescription_en+.%0D%0A+++++%3Fperson+dbo%3AknownFor+%3FknownFor+.%0D%0A+++++FILTER+%28LANG%28%3Fdescription_en%29+%3D+%27en%27%29+.%0D%0A%7D%0D%0Agroup+by+%3Fname+%3Fdescription_en+%3Fperson+%3FbirthName%0D%0AORDER+BY+%3Fname%0D%0ALIMIT+" + limit + "&output=json"
link = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Fname+%3FbirthName+%28group_concat%28%3FbirthDate%3Bseparator%3D%27%3B%27%29+as+%3FbirthDate%29+%3Fperson+%3Fdescription_en+WHERE+%7B%0D%0A+++++%3Fperson+dbo%3AbirthDate+%3FbirthDate+.%0D%0A+++++%3Fperson+dbo%3AbirthName+%3FbirthName+.%0D%0A+++++%3Fperson+foaf%3Aname+%3Fname+.%0D%0A+++++%3Fperson+rdfs%3Acomment+%3Fdescription_en+.%0D%0A+++++FILTER+%28LANG%28%3Fdescription_en%29+%3D+%27en%27%29+.%0D%0A%7D%0D%0Agroup+by+%3Fname+%3Fdescription_en+%3Fperson+%3FbirthName%0D%0AORDER+BY+%3Fname%0D%0ALIMIT+" + limit + "&output=json"
link = link.replace("birthDate", property)
data = json.load(urllib2.urlopen(link))

rawpeople = data["results"]["bindings"]
people = []
for rawperson in rawpeople:
	person = {}
	for p in rawperson.keys():
		person[p] = rawperson[p]["value"]
	people.append(person)
found = 0
cases = 0
for person in people:
	things = person[property].split(";")
	if type == "date":	# List of dates
		things = map(lambda x: x[0:4], things)
	elif type == "link":	# List of links
		things = map(lambda x: x.split("/")[-1].replace("_", " "), things)
	elif type == "string":
		pass
	else:
		warning("Unknown type. Select date or link")
	things = list(set(things))
	text = person["description_en"]
	for thing in things:
		cases += 1
		try:
			index = text.index(thing)
			lower = max(index - AROUND, 0)
			upper = min(index + len(thing) + AROUND, len(text))
			print(thing + " ; " + text[lower:upper])
			found += 1
		except ValueError:
			warning("\"" + thing + "\" not found in " + person["name"] + " abstract.")

warning(str(property) + " was found in " + str(found) + "/" + str(cases) + " cases.")