#!/usr/bin/env python


from collections import defaultdict
from math import log10

class Polarity(object):
    """docstring for Polarity"""
    def __init__(self, pos_words_path, neg_words_path, corpus_path, window=5):
        self.pos_words_path = pos_words_path
        self.neg_words_path = neg_words_path
        self.corpus_path = corpus_path
        self.window = window
        self.pos_word_list = self.retrieve_words(pos_words_path)
        self.neg_word_list = self.retrieve_words(neg_words_path)
        self.corpus_word_dict = dict()
        self.corpus_word_list = list()
        self.tolerance = 0.01
        self.retrieve_corpus()

    def get_pos_word_list(self):
        return self.pos_word_list

    def get_neg_word_list(self):
        return self.neg_word_list

    def get_corpus_word_list(self):
        return self.corpus_word_list

    def get_corpus_word_dict(self):
        return self.corpus_word_dict

    def get_tolerance(self):
        return self.tolerance

    def get_window(self):
        return self.window

    def set_tolerance(self, new_tolerance):
        self.tolerance = new_tolerance

    def set_window(self, new_window):
        self.window = new_window

    def retrieve_words(self, filename):
        word_list = list()
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                word_list.append(line)
        return word_list

    def retrieve_corpus(self):
        line_number = int()
        lines = str()
        with open(self.corpus_path) as f:
            #self.corpus_word_list = f.read().split()
            for line in f:
                lines += line
                line = line.split()
                line_number += 1
                self.corpus_word_dict[line_number] = line
        self.corpus_word_list = lines.split()

    def hits(self, of_word="excellent"):
        sentence_number = int()
        freq_each = int()
        freq_total = int()
        for k, v in self.corpus_word_dict.iteritems():
            sentence_number = k
            self.corpus_word_list.append(v)
            freq_each = v.count(of_word)
            freq_total += freq_each
            # print "hits({}) in sentence {} is {}".format(of_word, sentence_number, freq_each)
        return freq_total + self.get_tolerance()

    def hits_nearing(self, nearing_word, keyword="excellent"):
        """ USAGE:
        For positive polarity: only the nearing word needs to be given.

        For negative polarity: plus the nearing word, the parameters keyword and polarity
        should be set to "poor" and "neg", respectively."""
        hit = int()
        indices_of_nearing_word = list()
        # if polarity != "pos":
        #     word_list = self.neg_word_list
        # else:
        #     word_list = self.pos_word_list
        # for word in word_list:
        if nearing_word in self.corpus_word_list:
            indices_of_nearing_word = self.get_indices(nearing_word)
            window_to_consider = self.create_window(indices_of_nearing_word)
            if keyword in window_to_consider:
                hit += 1
        return hit + self.get_tolerance()

    def get_indices(self, word):
        """Returns a list of number/s representing index/indices of a word
        in the given word list, if it occurs in it; empty list, otherwise."""
        result = list()
        offset = -1
        while True:
            try:
                offset = self.get_corpus_word_list().index(word, offset+1)
            except ValueError:
                return result
            result.append(offset)

    def create_window(self, indices):
        certain_window = list()
        for index in indices:
            left_window = self.get_corpus_word_list()[index-self.get_window():index]
            right_window = self.get_corpus_word_list()[index+1:index+self.get_window()+1]
            certain_window += (left_window + right_window)
        return certain_window

    def evaluate_semantic_orientation(self, word):
        numerator = self.hits_nearing(word) * self.hits(of_word="poor")
        denominator = self.hits_nearing(word, keyword="poor") * self.hits()
        return log10(numerator/denominator)

    def run(self):
        l = []
        pos_word_list = self.get_pos_word_list()
        neg_word_list = self.get_neg_word_list()
        pos_neg = [pos_word_list, neg_word_list]
        for word_list in pos_neg:
            for elem in word_list:
                l.append(self.evaluate_semantic_orientation(elem))
        print list(set(sorted(l)))

#print get_words("opinion-lexicon-English/positive-words.txt")
#print get_corpus("testing.txt")

sample = Polarity("opinion-lexicon-English/positive-words.txt", "opinion-lexicon-English/negative-words.txt", "sample.preprocessed.txt")
# print sample.create_window(sample.get_indices('music'))
# print sample.hits_nearing('music', 'poor')
print sample.run()
