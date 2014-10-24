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

hmm = subprocess.Popen(["/Applications/Mathematica.app/Contents/MacOS/MathematicaScript", "-script", "UncoverHiddenStates"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
try:
	kattismatrix(a, hmm.stdin)
	kattismatrix(b, hmm.stdin)
	kattismatrix(q, hmm.stdin)

	for person in people:
		text = person["description_en"]
		tokens = tokenizer.tokenize(text)
		hmm.stdin.write(" ".join([str(toState(token, wordlist)) for token in tokens]))
		result = hmm.stdout.readline()
		print(result)
		result = [int(word) for word in result.split(" ")]
		print(person["name"] + " should be born " + person[property])
		for i, state in enumerate(result):
			if state == 2:
				sys.stdout.write(" " + tokens[i])
		sys.stdout.write("\n")
except:
	pass
finally:
	hmm.stdin.close()
	hmm.terminate()
