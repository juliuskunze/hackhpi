from typing import List, Tuple


def generate_html(sentences: List[List[Tuple[str, int, str]]]) -> str:
    result = """<!DOCTYPE html>
        <html>
        <head>
        <style>
        .word0 {
            color: grey;
        }
        div[class^="word"]{
            color: black;
            position: relative;
            display: inline-block
        }
        div[class^="word"] .tooltiptext {
            visibility: hidden;
            width: 120px;
            background-color: black;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 100%;
            left: 50%;
            margin-left: -60px;

            /* Fade in tooltip - takes 0.5 second to go from 0% to 100% opac: */
            opacity: 0;
            transition: opacity 0.5s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

        </style>
        </head>
        <body>
        """
    for sentence in sentences:
        for word, importance, ctag in sentence:
            result += "" \
                      "<div class=\"word{0}\">{1} \
                       <span class=\"tooltiptext\">{2}</span> \
                       </div>".format(str(importance), word, ctag)
            result += " "

    result += """
        </body>
        </html>
        """

    return result
