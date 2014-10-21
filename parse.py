import json
import sys
import re
import string
import operator
from collections import defaultdict

def warning(str):
	sys.stderr.write("\033[91m" + str + "\n\033[95m")

raw = sys.stdin.read()
people = json.loads(raw)

AROUND = 3
DISTINCT_WORDS = 200

property = sys.argv[1]
type = sys.argv[2]

countall = defaultdict(lambda: 0)
countpostfix = defaultdict(lambda: 0)		# word: count
counttarget = defaultdict(lambda: 0)
countprefix = defaultdict(lambda: 0)
countbackground = defaultdict(lambda: 0)

stripNonAlphaNumRe = re.compile('[^\w \d]+')

def addWord(word, countmap, globalcountmap=None, count=1):
	countmap[word] += count
	if globalcountmap == None:
		return
	globalcountmap[word] += count

def addWordOrNum(won, countmap, globalcountmap=None, count=1):
	if won.isalpha():
		addWord(won, countmap, globalcountmap, count)
	else:
		addWord('1', countmap, globalcountmap, count)

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
	inittext = person["description_en"]
	inittext = stripNonAlphaNumRe.sub('', inittext).lower()
	for thing in things:
		text = inittext;
		foundCount = 0
		try:
			while True:
				index = text.index(thing)
				prefix = text[0:index]
				text = text[index + len(thing):]
				prefix = prefix.split(" ")
				postfix = text.split(" ")[:AROUND]
				text = text[len(" ".join(postfix)):]
				foundCount += 1
				for word in postfix:
					addWordOrNum(word, countpostfix, countall)
				for word in prefix[-AROUND:]:
					addWordOrNum(word, countprefix, countall)
				for word in prefix[:-AROUND]:
					addWordOrNum(word, countbackground, countall)
		except ValueError:
			if foundCount == 0:
				warning("\"" + thing + "\" not found in " + person["name"] + " abstract.")
		for word in thing.split(" "):
			addWordOrNum(word, counttarget, countall, foundCount)
		for word in text.split(" "):
			addWordOrNum(word, countbackground, countall)

countall = sorted(countall.items(), key=operator.itemgetter(1))[:DISTINCT_WORDS]
words = [w[0] for w in countall]
states = [countbackground, countprefix, counttarget, countpostfix]
def stateToBCol(state, words):
	col = [state[word] for word in words]
	for word in words:
		del state[word]
	col.append(sum(state.values()))
	normalization = sum(col)
	return [float(count) / normalization for count in col]
b = [stateToBCol(state, words) for state in states]

for b2 in b:
	print(b2)
