from typing import Tuple, List

import nltk


def sentences_from_conll(
        file: str = '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll') -> List[List[Tuple[str, int, str]]]:
    data = open(file).read()
    sentence_graphs = list(nltk.parse.DependencyGraph(tableString) for tableString in data.split('\n\n'))

    return list(words_with_importance_from(sentence_graph) for sentence_graph in sentence_graphs)


def words_with_importance_from(sentence_graph: nltk.parse.DependencyGraph) -> List[Tuple[str, int, str]]:
    return list((node['word'], len(node['deps'].values()), node['ctag']) for node in sentence_graph.nodes.values())[
           1:]
