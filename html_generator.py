from typing import List, Tuple


def generate_html(sentences: List[List[Tuple[str, int]]]) -> str:
    result = """<!DOCTYPE html>
        <html>
        <head>
        <style>
        .word0 {
            color: grey;
        }
        .word*{
            color: black;
        }
        </style>
        </head>
        <body>
        """
    for sentence in sentences:
        for word, importance in sentence:
            result += "<span class=\"word{0}\">{1}</span>".format(str(importance), word)
            result += " "

    result += """
        </body>
        </html>
        """

    return result
