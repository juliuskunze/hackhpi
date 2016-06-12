# use this to configure (once):
# nltk.download()
from conll import sentences_from_conll
from html_generator import generate_html
from parsey import generate_conll_file


def generate_html_file(input_conll_file: str, output_html_file: str):
    result = sentences_from_conll()
    html = generate_html(result)
    target = open(output_html_file, 'w')
    target.write(html)
    target.close()


generate_html_file(input_conll_file=generate_conll_file(), output_html_file="format.html")
