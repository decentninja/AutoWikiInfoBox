import sys
import re
import string

def tokenize(text):
	stripNonAlphaNumRe = re.compile('[^\w\- \d]+')
	text = stripNonAlphaNumRe.sub('', text).lower()
	return text.split(" ")
