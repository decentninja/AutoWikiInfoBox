import sys
import re
import string

text = sys.stdin.read()

stripNonAlphaNumRe = re.compile('[^\w\- \d]+')
text = stripNonAlphaNumRe.sub('', text).lower()
split_text = text.split(" ")
for word in split_text:
	if word.isalpha() :
		sys.stdout.write(word+" ")
	else :
		sys.stdout.write("1")
