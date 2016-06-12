from typing import List

import nltk

from word2vec import frequencies


class WordInfo:
    def __init__(self, word: str, child_count: int, word_class: str, nesting_level: int = 0, is_special: bool = False):
        self.frequency = frequencies.frequency(word) * 100
        self.uniqueness =  1 / self.frequency if (self.frequency != 0) else 1
        self.word = word
        self.word_class = word_class
        self.nesting_level = nesting_level
        self.is_root_noun = word_class == 'NOUN' and nesting_level == 2
        self.is_root_verb = word_class == 'VERB' and nesting_level == 1
        self.is_not = (word.lower() if word else None) == 'not'
        self.is_special = is_special  # e.g. name


def sentences_from_conll(file: str = '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll') -> List[
    List[WordInfo]]:
    data = open(file).read()
    sentence_graphs = list(sentence_graph for sentence_graph in
                           list(nltk.parse.DependencyGraph(tableString) for tableString in data.split('\n\n')) if
                           sentence_graph.root != None)

    for sentence_graph in sentence_graphs:
        sentence_graph.root['nesting_level'] = 0
        none_count = None
        while True:
            none_count_new = len(list(node for node in sentence_graph.nodes.values() if 'nesting_level' in node))
            if none_count_new == none_count:
                break

            none_count = none_count_new

            for node in sentence_graph.nodes.values():
                if 'nesting_level' in node:
                    children_indices = list(index for value in node['deps'].values() for index in value)
                    for index in children_indices:
                        child = sentence_graph.nodes[index]
                        next = node['nesting_level'] + 1
                        child['nesting_level'] = min(child['nesting_level'], next) if (
                            'nesting_level' in child) else next

    with open('highlighting/wordlist2.txt') as wordlist:
        knownWords = set(line.rstrip().lower() for line in wordlist)

    return list(words_with_importance_from(sentence_graph, knownWords) for sentence_graph in sentence_graphs)


def words_with_importance_from(sentence_graph: nltk.parse.DependencyGraph, knownWords) -> List[WordInfo]:
    return list(WordInfo(word=node['word'],
                         child_count=len(node['deps'].values()),
                         word_class=node['ctag'],
                         nesting_level=node['nesting_level'] if ('nesting_level' in node) else None) for node in
                sentence_graph.nodes.values())[1:]

    # is_special=(re.sub('[^a-z]', '', node['word'].lower()) in knownWords)
