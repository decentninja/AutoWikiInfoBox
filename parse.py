import json
import sys


def warning(str):
	sys.stderr.write("\033[91m" + str + "\n\033[95m")

raw = sys.stdin.read()
people = json.loads(raw)

AROUND = 3

property = sys.argv[1]
type = sys.argv[2]

allpostfix = {}		# word: count

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
		try:
			index = text.index(thing)
			prefix = text[0:index]
			postfix = text[index + len(thing):]
			prefixwords = prefix.split(" ")[AROUND:]
			postfix = postfix.split(" ")[:AROUND]
			for word in postfix:
				word = word.lower()
				if word in allpostfix:
					allpostfix[word] += 1
				else:
					allpostfix[word] = 1
		except ValueError:
			warning("\"" + thing + "\" not found in " + person["name"] + " abstract.")

print(allpostfix)