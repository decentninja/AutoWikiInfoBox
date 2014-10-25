import re
import sys


def tokenize(text):
	stripNonAlphaNumRe = re.compile('[^\w\- \d]+')
	text = stripNonAlphaNumRe.sub('', text).lower()
	return text.split(" ")

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