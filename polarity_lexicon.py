#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import exit, argv
from pickle import dump
from math import log10
from pprint import pprint

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
    self.resultant = dict()

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

  def get_resultant(self):
    return self.resultant

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
    # sentence_number = int()
    # freq_each_line = int()
    # freq_total = int()
    # for key, value in self.get_corpus_word_dict().iteritems():
    #   sentence_number = key
    #   # ??? REDUNDANT
    #   # self.corpus_word_list.append(value)
    #   freq_each_line = value.count(of_word)
    #   freq_total += freq_each_line
    # # print "hits({}) in sentence {} is {}".format(of_word, sentence_number, freq_each_line)
    freq_total = self.get_corpus_word_list().count(of_word)
    return freq_total + self.get_tolerance()

  def hits_nearing(self, nearing_word, keyword="excellent"):
    """USAGE:
    For positive polarity: only the nearing word needs to be given.

    For negative polarity: in addition to the nearing word,
    the parameter 'keyword' should be set to 'poor'."""
    hit = int()
    indices_of_nearing_word = list()
    if nearing_word in self.get_corpus_word_list():
      indices_of_nearing_word = self.get_indices(nearing_word)
      window_to_consider = self.create_window(indices_of_nearing_word)
      if keyword in window_to_consider:
        hit += window_to_consider.count(keyword)
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
    ctrl = 0
    result_pos, result_neg = list(), list()
    pos_word_list = self.get_pos_word_list()
    neg_word_list = self.get_neg_word_list()
    pos_neg = [pos_word_list, neg_word_list]
    for word_list in pos_neg:
      for word in word_list:
        eval_SO = self.evaluate_semantic_orientation(word)
        self.get_resultant()[word] = eval_SO
        if ctrl == 0:
          result_pos.append(eval_SO)
        else:
          result_neg.append(eval_SO)
      ctrl = -1
    accuracy_pos = float(len([i for i in result_pos if i > 0]))/len(pos_word_list)
    accuracy_neg = float(len([i for i in result_neg if i < 0]))/len(neg_word_list)
    print "-------------"
    print "accuracy of pos: ", accuracy_pos
    print "accuracy of neg: ", accuracy_neg
    print '\n'
    print "list of sorted set of pos: ", list(sorted(set(result_pos)))
    print "list of sorted set of neg: ", list(sorted(set(result_neg)))
    print '\n'
    pprint(self.get_resultant())
    self.write_to_file()
    return (accuracy_neg + accuracy_pos)/2

  def write_to_file(self):
    output = open('polarity-output.pkl', 'wb')
    dump(self.get_resultant(), output)
    output.close()

def main():
  pos_words = raw_input("Please provide the path for positive words' lexicon:\n")
  print '\n'
  neg_words = raw_input("Please provide the path for negative words' lexicon:\n")
  print '\n'
  corpus = raw_input("Please finally provide the path for corpus:\n")
  instance = Polarity(pos_words, neg_words, corpus)
  print instance.run()

if __name__ == '__main__':
    exit(main())