from sys import argv
import re

print "Usage:	python highlighting.py data/nytimes.txt"

script, filename = argv

with open('wordlist.txt') as wordlist:
	keywords1 = set(line.rstrip().lower() for line in wordlist)
with open('wordlist2.txt') as wordlist:
	keywords2 = set(line.rstrip().lower() for line in wordlist) #could be enough
keywords = keywords1.union(keywords2)
	
with open(filename, 'r') as fileIn:
	with open(filename+'.out', 'w') as fileOut:
		for line in fileIn:
			#words = re.findall(r"[\w']+", line)
			words = re.split('(\W)', line)
			lineOut = ''
			for word in words:
				word2 = re.sub('[^a-z]', '', word.lower())
				if word2 not in keywords:
					print "<mark>" + word + "</mark>"
					lineOut += "<mark>" + word + "</mark>"
				else:
					lineOut += word
			
			fileOut.write(lineOut)
	