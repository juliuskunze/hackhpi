from typing import Tuple, List

import nltk


def sentences_from_conll(
        file: str = '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll') -> List[List[Tuple[str, int]]]:
    data = open(file).read()
    sentence_graphs = list(nltk.parse.DependencyGraph(tableString) for tableString in data.split('\n\n'))

    return list(words_with_importance_from(sentence_graph) for sentence_graph in sentence_graphs)


def words_with_importance_from(sentence_graph: nltk.parse.DependencyGraph) -> List[Tuple[str, int]]:
    return list((node['word'], len(node['deps'].values())) for node in sentence_graph.nodes.values())[1:]

# def dependants(sentence_graph: nltk.parse.DependencyGraph) -> List[Tuple[str, int]]:
#     flattened_children = list(child for node in sentence_graph.nodes.values() for children in node['deps'].values() for child in children)
#     counter = Counter(flattened_children)
#     occurrence_count= list(counter[i] for i in sentence_graph.nodes.keys())
#     return list((sentence_graph.nodes[index]['word'], count) for index, count in enumerate(occurrence_count))
