import json
import sys
import subprocess
import helpers
import re


pattern=re.compile("[0-9]{4}")		# Regex for comparison

def toState(token, wordlist):
	try:
		if not token.isalpha():
			return wordlist.index("1")
		return wordlist.index(token)
	except ValueError:
		# This assumes that the last type of emission is the unknown emission,
		# and that it isn't contained in the wordlist
		return len(wordlist)

def kattismatrix(matrix, stream):
	stream.write(str(len(matrix)) + " " + str(len(matrix[0])))
	for r in matrix:
		for c in r:
			stream.write(" " + str(c))
	stream.write("\n")

property = sys.argv[1]
type = sys.argv[2]

raws = sys.stdin.readlines()
indata = [json.loads(raw) for raw in raws]

people = indata[0]
a = indata[1]
b = indata[2]
q = indata[3]
wordlist = indata[4]

states = ["back", "pre", "target", "post"]

hmm = subprocess.Popen(["./viterbi"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
hits = 0
incorrect = 0
notfound = 0
regexnotfound = 0
regexincorrect = 0
regexhits = 0
try:
	kattismatrix(a, hmm.stdin)
	kattismatrix(b, hmm.stdin)
	kattismatrix(q, hmm.stdin)

	run = False
	for person in people:
		run = not run
		if run:
			continue
		text = person["description_en"]
		tokens = helpers.tokenize(text)
		hmm.stdin.write(str(len(tokens)) + " " + " ".join([str(toState(token, wordlist)) for token in tokens]) + "\n")
		result = hmm.stdout.readline()
		result = [int(word) for word in result.split(" ")]
		values = [helpers.extract(x, type) for x in person[property].split(";")]
		weguessed = False
		correct = False

		# The regex guess
		r = pattern.search(person["description_en"])
		regexguess = None
		if r:
			regexguess = r.group(0)
			if regexguess in values:
				regexhits += 1
			else:
				regexincorrect += 1
		else:
			regexnotfound += 1

		debug = ""
		ourguess = ""
		for i, state in enumerate(result):
			debugstyle = ""
			if tokens[i] in values:
				debugstyle += '\033[4m'
			if regexguess and tokens[i] == regexguess:
				debugstyle += "r"
			if state == 1:
				debugstyle += '\033[90m'
			if state == 2:
				debugstyle += '\033[91m'
			if state == 3:
				debugstyle += '\033[92m'
			debug += debugstyle + tokens[i] + '\033[0m' + " "

			if state == 2:
				weguessed = True
				ourguess += (tokens[i]+" ")

		for value in values:
			correct = True
			for word in re.split('\W+', value.lower()):
				if (word=='actor' or word=='actress'):
					if ourguess.find('actor')== -1 and ourguess.find('actress') == -1:
						correct = False
				elif (word != 'and') and ourguess.find(word) == -1:
					correct = False
			if correct:
				break
		debug += "\n"


		if not weguessed:
			notfound += 1
			print("\033[92mNot found: \033[0m" + debug)
		elif correct:
			hits += 1
			print("\033[4m\033[91mCorrect\033[0m: " + debug)
		else:
			print("\033[93mIncorrect:\033[0m " + debug)
			print map(lambda s: s.lower(), values),
			print("\n")
			incorrect += 1

finally:
	hmm.stdin.close()
	hmm.terminate()
print("Stat        HMM\t\tRegex")
print("Correct:    " + str(hits)) + "\t\t" + str(regexhits)
print("Incorrect:  " + str(incorrect)) + "\t" + str(regexincorrect)
print("Not found:  " + str(notfound)) + "\t\t" + str(regexnotfound)
print("Total num people searched: " + str(len(people)/2))
