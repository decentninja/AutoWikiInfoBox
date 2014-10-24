import json
import sys
import subprocess
import tokenizer

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

raws = sys.stdin.readlines()
indata = [json.loads(raw) for raw in raws]

people = indata[0]
a = indata[1]
b = indata[2]
q = indata[3]
wordlist = indata[4]

states = ["back", "pre", "target", "post"]

hmm = subprocess.Popen(["./searcher"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
hits = 0
incorrect = 0
misses = 0
try:
	kattismatrix(a, hmm.stdin)
	kattismatrix(b, hmm.stdin)
	kattismatrix(q, hmm.stdin)

	for person in people:
		text = person["description_en"]
		tokens = tokenizer.tokenize(text)
		hmm.stdin.write(str(len(tokens)) + " " + " ".join([str(toState(token, wordlist)) for token in tokens]) + "\n")
		result = hmm.stdout.readline()
		result = [int(word) for word in result.split(" ")]
		year = person[property][:4]
		sys.stdout.write(year)
		hasHit = False
		for i, state in enumerate(result):
			if state == 2:
				hasHit = True
				sys.stdout.write(" " + tokens[i])
				if year == tokens[i]:
					hits += 1
				else:
					incorrect += 1
		if not hasHit:
			misses += 1
		sys.stdout.write("\n")
finally:
	hmm.stdin.close()
	hmm.terminate()
print("num people: " + str(len(people)))
print("hits: " + str(hits))
print("incorrect: " + str(incorrect))
print("misses: " + str(misses))
