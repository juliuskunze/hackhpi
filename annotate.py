import sys

from lxml.etree import _Element
from lxml.html import html5parser
from html5lib import HTMLParser

root = html5parser.parse('data/article.html', parser=HTMLParser(namespaceHTMLElements=False))

def find_paragraphs(elem: _Element):
    ps = elem.find('p')
    f = open('input.txt', mode='w')
    for p in ps:
        f.write(p.text + '\n')
    f.close()

find_paragraphs(root)