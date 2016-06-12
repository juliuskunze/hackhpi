from typing import List

import nltk


class WordInfo:
    def __init__(self, word: str, child_count: int, word_class: str, nesting_level: int = 0):
        self.word = word
        self.importance = child_count
        self.word_class = word_class
        self.nesting_level = nesting_level
        self.is_root_subject = word_class == 'NOUN' and nesting_level == 1
        self.is_root_verb = word_class == 'VERB' and nesting_level == 0


def sentences_from_conll(file: str = '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll') -> List[WordInfo]:
    data = open(file).read()
    sentence_graphs = list(nltk.parse.DependencyGraph(tableString) for tableString in data.split('\n\n'))

    return list(words_with_importance_from(sentence_graph) for sentence_graph in sentence_graphs)


def words_with_importance_from(sentence_graph: nltk.parse.DependencyGraph) -> List[WordInfo]:
    return list(WordInfo(word=node['word'], child_count=len(node['deps'].values()), word_class=node['ctag']) for node in
                sentence_graph.nodes.values())[
           1:]
