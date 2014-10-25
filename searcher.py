import json
import sys
import subprocess
import helpers

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
try:
	kattismatrix(a, hmm.stdin)
	kattismatrix(b, hmm.stdin)
	kattismatrix(q, hmm.stdin)

	for person in people:
		text = person["description_en"]
		tokens = helpers.tokenize(text)
		hmm.stdin.write(str(len(tokens)) + " " + " ".join([str(toState(token, wordlist)) for token in tokens]) + "\n")
		result = hmm.stdout.readline()
		result = [int(word) for word in result.split(" ")]
		values = [helpers.extract(x, type) for x in person[property].split(";")]
		weguessed = False
		correct = False
		debug = ""
		for i, state in enumerate(result):
			debugstyle = ""
			if tokens[i] in values:
				debugstyle += '\033[4m'
			if state == 1:
				debugstyle += '\033[90m'
			if state == 2:
				debugstyle += '\033[91m'
			if state == 3:
				debugstyle += '\033[92m'
			debug += debugstyle + tokens[i] + '\033[0m' + " "

			if state == 2:
				weguessed = True
				ourguess = tokens[i]
				for value in values:
					if value == tokens[i]:
						correct = True
		debug += "\n"
		if not weguessed:
			notfound += 1
			print("\033[92mNot found: \033[0m" + debug)
		elif correct:
			hits += 1
			print("\033[4m\033[91mCorrect\033[0m: " + debug)
		else:
			print("\033[93mIncorrect:\033[0m " + debug)
			incorrect += 1
finally:
	hmm.stdin.close()
	hmm.terminate()
print("Num people: " + str(len(people)))
print("Correct: " + str(hits))
print("Incorrect: " + str(incorrect))
print("Not found: " + str(notfound))
