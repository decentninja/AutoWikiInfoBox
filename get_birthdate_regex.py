import json
import urllib2
import sys
import dateutil.parser as dup
import re

pattern=re.compile("[0-9]{4}")

def get(property, limit):
	link = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Fname+%3FbirthName+%28group_concat%28%3FbirthDate%3Bseparator%3D%27%3B%27%29+as+%3FbirthDate%29+%3Fperson+%3Fdescription_en+WHERE+%7B%0D%0A+++++%3Fperson+dbo%3AbirthDate+%3FbirthDate+.%0D%0A+++++%3Fperson+dbo%3AbirthName+%3FbirthName+.%0D%0A+++++%3Fperson+foaf%3Aname+%3Fname+.%0D%0A+++++%3Fperson+rdfs%3Acomment+%3Fdescription_en+.%0D%0A+++++FILTER+%28LANG%28%3Fdescription_en%29+%3D+%27en%27%29+.%0D%0A%7D%0D%0Agroup+by+%3Fname+%3Fdescription_en+%3Fperson+%3FbirthName%0D%0AORDER+BY+%3Fname%0D%0ALIMIT+" + str(limit) + "&output=json"
	link = link.replace("birthDate", property)
	raw = json.load(urllib2.urlopen(link))
	return raw
		
def parse_and_count(raw):
	count = 0
	rawpeople = raw["results"]["bindings"]
	for rawperson in rawpeople:
		for p in rawperson.keys():
			if p == "birthDate":
				birthYear=rawperson[p]["value"][0:4]
			if p == "description_en" :
				descr = rawperson[p]["value"]
		#Checks birthYear with regex
		pos=pattern.search(descr)
		if pos != None:
			if pos.group(0) == birthYear:
				count=count+1	
	return count
	
property = sys.argv[1]
limit = 100
if len(sys.argv) >= 3:
	limit = sys.argv[2]
people = parse_and_count(get(property, limit))
print(people)
