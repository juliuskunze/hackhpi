from typing import List

from conll_reader import WordInfo

halfGray = 0xd3d3d3


def brightness_from_frequency(freq: float) -> float:
    return .6 * (freq * 2) + .4


def generate_html(sentences: List[List[WordInfo]]) -> str:
    result = """<!DOCTYPE html>
        <html>
        <head>
        <style>
        div[class^=word].word0 {
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

        div[class^=word]:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
        </head>
        <body>
        """
    for sentence in sentences:
        for word in sentence:
            color = "color:red" if word.is_root_noun else "color:green" if word.is_root_verb else "color:blue" if word.is_special else "color:black;opacity:{0}".format(
                brightness_from_frequency(word.frequency))
            result += "" \
                      "<div class=\"word{0}\" style=\"{2}\">{1}&nbsp \
                       <span class=\"tooltiptext\">{3}</span> \
                       </div>".format('0', word.word, color,                                      "{1} ({0})".format(str(word.nesting_level), word.word_class))

    result += """
            </body>
            </html>
            """

    return result
