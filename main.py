import sys


def warning(str):
	sys.stderr.write("\033[91m" + str + "\n\033[95m")



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


if __name__ == "__main__":
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