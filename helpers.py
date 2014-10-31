import re
import sys

stripNonAlphaNumRe = re.compile('[^\w\- \d]+')
def tokenize(text):
	text = text.lower()

	text = re.sub(',', ' COMMA ', text)
	text = re.sub('\.', ' DOT ', text)
	text = re.sub('\(', ' OPENBRACKET ', text)
	text = re.sub('\)', ' CLOSEBRACKET ', text)
	text = re.sub(u'\u2013',' ENDASH ',text)
	text = re.sub(u'\u2012',' FIGDASH ',text)

	text = stripNonAlphaNumRe.sub(' ', text)
	return text.split()

def extract(thing, type):
	if type == "date":	# List of dates
		thing = thing[0:4]
	elif type == "link":	# List of links
		thing = thing.split("/")[-1].replace("_", " ")
	elif type == "string":
		pass
	else:
		warning("Unknown type")
	return thing

def warning(s):
	sys.stderr.write("\033[91m" + s + "\n\033[95m")
