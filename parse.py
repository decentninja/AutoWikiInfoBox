import json
import sys
import re
import string


def warning(str):
	sys.stderr.write("\033[91m" + str + "\n\033[95m")

raw = sys.stdin.read()
people = json.loads(raw)

AROUND = 3

property = sys.argv[1]
type = sys.argv[2]

allcount = {}
allpostfix = {}		# word: count
allprefix = {}
allcorrect = {}
allbackground = {}

stripNonAlphaNumRe = re.compile('[^\w \d]+')

def addWord(word, countmap, globalcountmap=None):
	if word in countmap:
		countmap[word] += 1
	else:
		countmap[word] = 1
	if not globalcountmap:
		return
	if word in globalcountmap:
		globalcountmap[word] += 1
	else:
		globalcountmap[word] = 1

def addWordOrNum(won, countmap, globalcountmap=None):
	if won.isalpha():
		addWord(won, countmap, globalcountmap)
	else:
		addWord('1', countmap, globalcountmap)

for person in people:
	things = person[property].split(";")
	if type == "date":	# List of dates
		things = map(lambda x: x[0:4], things)
	elif type == "link":	# List of links
		things = map(lambda x: x.split("/")[-1].replace("_", " "), things)
	elif type == "string":
		pass
	else:
		warning("Unknown type")
	things = list(set(things))
	text = person["description_en"]
	text = stripNonAlphaNumRe.sub('', text).lower()
	for thing in things:
		try:
			foundCount = 0
			while True:
				index = text.index(thing)
				prefix = text[0:index]
				text = text[index + len(thing):]
				prefix = prefix.split(" ")
				postfix = text.split(" ")[:AROUND]
				text = text[" ".join(postfix).__len__:]
				foundCount += 1
				for word in postfix:
					addWordOrNum(word, allpostfix, allcount)
				for word in prefix[-AROUND:]:
					addWordOrNum(word, allprefix, allcount)
				for word in prefix[:-AROUND]:
					addWordOrNum(word, allbackground, allcount)
		except ValueError:
			if foundCount == 0:
				warning("\"" + thing + "\" not found in " + person["name"] + " abstract.")
		for word in text.split(" "):
			addWordOrNum(word, allbackground, allcount)


