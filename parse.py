import json
import sys
import re
import string
import operator
from collections import defaultdict
from helpers import warning
import helpers


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

stripNonAlphaNumRe = re.compile('[^\w\- \d]+')	# This is incorrect, it will remove non-latin characters (unless python has a weird \w in regexes)

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

backtoback = 0
backtoprefix = 0
targettotarget = 0
targettopost = 0

run = True
for person in people:
	run = not run
	if run:
		continue
	things = person[property].split(";")
	things = map(lambda x: helpers.extract(x, type), things)
	things = [helpers.tokenize(thing) for thing in list(set(things))]
	thingsFound = [0 for thing in things]
	text = helpers.tokenize(person["description_en"])
	prevPostEnd = 0
	currWord = 0
	while currWord < len(text):
		for i, thing in enumerate(things):
			if thing[thingsFound[i]] != text[currWord]:
				thingsFound[i] = 0
				continue
			thingsFound[i] += 1
			if thingsFound[i] < len(thing):
				continue

			start = currWord - len(thing) + 1

			backtoback += max(0, start - AROUND) - prevPostEnd - 1
			for word in text[prevPostEnd : max(0, start - AROUND)]:
				addWordOrNum(word, countbackground)

			backtoprefix += 1
			for word in text[max(0, start - AROUND):max(0, start)]:
				addWordOrNum(word, countprefix, countall)

			targettotarget += currWord+1 - start - 1
			for word in text[start : currWord+1]:
				addWordOrNum(word, counttarget, countall)

			targettopost += 1
			prevPostEnd = min(len(text), currWord + AROUND + 1)
			for word in text[currWord+1 : prevPostEnd]:
				addWordOrNum(word, countpostfix, countall)

			currWord = prevPostEnd - 1
			for j in range(0, len(thingsFound)):
				thingsFound[j] = 0
			break
		currWord += 1

	if prevPostEnd == 0:
		warning("None of \"" + (",".join([" ".join(t) for t in things])) + "\" found in " + person["name"] + " abstract.")
	backtoback += len(text) - prevPostEnd
	for word in text[prevPostEnd : len(text)]:
		addWordOrNum(word, countbackground)

countall = sorted(countall.items(), key=operator.itemgetter(1), reverse=True)[:DISTINCT_WORDS]
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


s = 0.0 + backtoback + backtoprefix
backtoback /= s
backtoprefix /= s
s = 0.0 + targettopost + targettotarget
targettopost /= s
targettotarget /= s
a = [
	[backtoback, backtoprefix, 0.0, 0.0],
	[0.0, (AROUND-1.0)/AROUND, 1.0/AROUND, 0.0],
	[0.0, 0.0, targettotarget, targettopost],
	[1.0/AROUND, 0.0, 0.0, (AROUND-1.0)/AROUND]
]

q = [[1.0, 0.0, 0.0, 0.0]]

print(json.dumps(a))
print(json.dumps(b))
print(json.dumps(q))
print(json.dumps(words))

