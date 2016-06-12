import heapq
import logging
import os
import re
import time
from collections import Counter
from typing import List, Iterable, Tuple, Dict

import gensim
from numpy.core.multiarray import dot

from operator import itemgetter

REG_MATCH_DBP = re.compile(r'DBP:[^\s]+')

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
            return 0


def word_frequencies(words: List[str], cut_off_most_common: int = 100) -> WordFrequencies:
    total_count = len(words)
    counter = Counter(words).items()
    frequency_by_word = dict((word, value / total_count) for word, value in counter)

    return WordFrequencies(frequency_by_word, cut_off_most_common=cut_off_most_common)


def word_frequencies_from_sentences(sentences: Iterable[Iterable[str]]) -> WordFrequencies:
    return word_frequencies(list(value for v in sentences for value in v))

class Word2VecModel:
    def __init__(self, model: gensim.models.Word2Vec = None):
        self.model = model
        self.trained_duration = None
        pass

    @classmethod
    def load(cls, file: str, use_binary=False):
        logging.info('Loading {}'.format(file))
        gensim_model = None
        if use_binary:
            gensim_model = gensim.models.Word2Vec.load_word2vec_format(file, binary=True)
        else:
            gensim_model = gensim.models.Word2Vec.load(file)
        m = cls(gensim_model)
        logging.info('Loaded')
        return m

    def word_frequencies(self, cut_off_most_common: int = 100) -> WordFrequencies:
        return WordFrequencies(
            dict((word, self.model.vocab[word].count / self.model.corpus_count) for word in self.model.vocab),
            cut_off_most_common=cut_off_most_common)

    def continue_training(self, sentences, thread_count=48, min_count=10, batch_words=1000000, iterations=5):
        self.model.workers = thread_count
        self.model.min_count = min_count
        self.model.batch_words = batch_words
        self.model.iter = iterations
        self.model.train(sentences)

    @classmethod
    def trained(cls, sentences, thread_count=48, min_count=10, batch_words=1000000, iterations=5):
        logging.info('Training using {} cores'.format(thread_count))
        start = time.time()
        model = cls(gensim.models.Word2Vec(
            sentences,
            workers=thread_count,
            trim_rule=cls._allow_dbp_references,
            min_count=min_count,
            batch_words=batch_words,
            iter=iterations
        ))
        end = time.time()
        model.trained_duration = end - start
        logging.info('Training done in {} seconds'.format(model.trained_duration))
        return model

    def save(self, file):
        logging.info('Storing model')
        start = time.time()
        self.model.save(file)
        end = time.time()
        saveDuration = end - start
        logging.info('Stored model in {} seconds'.format(saveDuration))
        return saveDuration

    @staticmethod
    def cosine_similarity(v1, v2):
        return dot(gensim.matutils.unitvec(v1), gensim.matutils.unitvec(v2))

    @staticmethod
    def _allow_dbp_references(word, count, min_count):
        if REG_MATCH_DBP.search(word) is not None:
            return gensim.utils.RULE_KEEP
        else:
            return gensim.utils.RULE_DEFAULT






class Sentences:
    def __init__(self, file_path: str, limit: int = None, blacklist: List[str] = []):
        self.file_path = file_path
        self.limit = limit
        self.blacklist = blacklist

    def __iter__(self) -> Iterable[List[str]]:
        i = 0
        for line in open(self.file_path, encoding='utf-8'):
            if self.limit and i > self.limit:
                return
            i += 1

            yield line_to_sentence(line, blacklist=self.blacklist)


def line_to_sentence(line: str, blacklist: List[str] = []) -> List[str]:
    line = line.lower().split()
    return [word for word in line if word not in blacklist]


class Word2VecModelStorage:
    def __init__(self, name, get_model=None, base_path='/home/julius/prj/knowledge-mining/data/'):
        self.file_sentences = '{}/{}.sentences'.format(base_path, name)
        self.file_model = '{}/{}.model'.format(base_path, name)
        self.trained_duration = None
        self.get_model = get_model or (lambda: Word2VecModel.trained(Sentences(self.file_sentences), CORE_COUNT))

    def train_and_save(self):
        m = self.get_model()
        m.save(self.file_model)
        return m

    def load(self):
        return Word2VecModel.load(self.file_model)

    def load_or_train(self):
        return self.load() if os.path.isfile(self.file_model) else self.train_and_save()

def first100k_model() -> Word2VecModel:
    return Word2VecModelStorage('data-first-100k').load_or_train()


frequencies = first100k_model().word_frequencies()