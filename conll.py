import nltk
from nltk.corpus import treebank
from nltk.corpus.reader import conll

nltk.download()
t = conll.ConllCorpusReader('/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll')[0]
t.draw()