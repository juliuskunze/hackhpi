import heapq
import logging
from collections import Counter
from operator import itemgetter
from typing import Iterable, List, Dict
from typing import Tuple


class WordFrequencies:
    def __init__(self, frequency_by_word: Dict[str, float], cut_off_most_common: int = 100):
        self.frequency_by_word = frequency_by_word
        for word in self.most_common_words(cut_off_most_common):
            del self.frequency_by_word[word]

    def most_common_words(self, n: int) -> List[str]:
        return list(word for word, frequency in self.most_common_frequencies_by_word(n))

    def most_common_frequencies_by_word(self, n: int = None) -> List[Tuple[int, str]]:
        if n is None:
            return sorted(self.frequency_by_word.items(), key=itemgetter(1), reverse=True)
        return heapq.nlargest(n, self.frequency_by_word.items(), key=itemgetter(1))

    def frequency(self, word: str) -> float:
        if word in self.frequency_by_word.keys():
            return self.frequency_by_word[word]
        else:
            logging.info("Word {} not found, returning frequency 0.".format(word))
            return 0


def word_frequencies(words: List[str], cut_off_most_common: int = 100) -> WordFrequencies:
    total_count = len(words)
    counter = Counter(words).items()
    frequency_by_word = dict((word, value / total_count) for word, value in counter)

    return WordFrequencies(frequency_by_word, cut_off_most_common=cut_off_most_common)


def word_frequencies_from_sentences(sentences: Iterable[Iterable[str]]) -> WordFrequencies:
    return word_frequencies(list(value for v in sentences for value in v))
