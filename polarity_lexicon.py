#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import exit
from json import dumps
from math import log10
from pprint import pprint
from collections import defaultdict

class Polarity:
  """Estimates each word's polarity using Turney's extended metric of PMI."""
  def __init__(self, pos_words_path, neg_words_path, corpus_path, window=5):
    self.pos_words_path = pos_words_path
    self.neg_words_path = neg_words_path
    self.corpus_path = corpus_path
    self.window = window
    self.pos_word_list = self.retrieve_words(pos_words_path)
    self.neg_word_list = self.retrieve_words(neg_words_path)
    self.corpus_word_dict = defaultdict(int)
    self.corpus_word_list = list()
    self.tolerance = 0.01
    self.retrieve_corpus()
    self.resultant_dict = dict()
    self.resultant_pos_list = list()
    self.resultant_neg_list = list()
    self.pos_dict = defaultdict(int)
    self.neg_dict = defaultdict(int)
    self.pinguin()

  def pinguin(self):
    """Makes the program ready to run---creates
    respective windows and fills in the dicts."""
    indices_of_excellent = self.get_indices('excellent')
    indices_of_poor = self.get_indices('poor')
    window_for_excellent = self.create_window(indices_of_excellent)
    window_for_poor = self.create_window(indices_of_poor)
    for word in window_for_excellent:
      self.pos_dict[word] += 1
    for word in window_for_poor:
      self.neg_dict[word] += 1
    for word in self.corpus_word_list:
      self.corpus_word_dict[word] += 1

  def retrieve_words(self, filename):
    """VOID. Returns a list of tokens of a given file."""
    word_list = list()
    with open(filename, 'r') as f:
      for line in f:
        line = line.strip()
        word_list.append(line)
    return word_list

  def retrieve_corpus(self):
    """VOID. Creates a list of tokens in the corpus."""
    with open(self.corpus_path) as f:
      self.corpus_word_list = f.read().split()

  def hits(self, of_word):
    """Returns a floating-point number that represents the
    occurrence of a given word in the corpus (+ tolerance value)."""
    return self.corpus_word_dict[of_word] + self.tolerance

  def hits_nearing(self, nearing_word, keyword):
    """Returns a floating-point number that represents
    how many times nearing_word and keyword co-occur
    (+ tolerance value)."""
    if keyword == 'poor':
      return self.neg_dict[nearing_word] + self.tolerance
    else:
      return self.pos_dict[nearing_word] + self.tolerance

  def get_indices(self, word):
    """Returns a list of integer/s representing index/indices of a word
    in the given word list, if it occurs in it; empty list, otherwise."""
    result = list()
    offset = -1
    while True:
      try:
        offset = self.corpus_word_list.index(word, offset+1)
      except ValueError:
        return result
      result.append(offset)

  def create_window(self, indices):
    """Consumes a list of integers that represent indices of
    a given word (either 'excellent' or 'poor', in this case)
    occurring in the corpus, and returns a list of strings
    that are within distance of as window (both lhs and rhs)
    to the word situated on that index."""
    certain_window = list()
    for index in indices:
      left_window = self.corpus_word_list[index-self.window:index]
      right_window = self.corpus_word_list[index+1:index+self.window+1]
      certain_window += (left_window + right_window)
    return certain_window

  def evaluate_semantic_orientation(self, word):
    """Calculates overall polarity of a given word."""
    numerator = self.hits_nearing(word, 'excellent') * self.hits('poor')
    denominator = self.hits_nearing(word, 'poor') * self.hits('excellent')
    return log10(numerator/denominator)

  def run(self):
    # Checks which of the two lists is handling,
    # positive=0 or negative=-1.
    ctrl = 0
    result_pos, result_neg = list(), list()
    pos_neg = [self.pos_word_list, self.neg_word_list]
    for word_list in pos_neg:
      if ctrl == 0:
        # if the word comes from the positive list
        for word in word_list:
          eval_SO = self.evaluate_semantic_orientation(word)
          self.resultant_dict[word] = eval_SO
          result_pos.append(eval_SO)
      else:
        # or from the negative list
        for word in word_list:
          eval_SO = self.evaluate_semantic_orientation(word)
          self.resultant_dict[word] = eval_SO
          result_neg.append(eval_SO)
      ctrl = -1
    accuracy_pos = float(len([i for i in result_pos if i > 0]))
    accuracy_neg = float(len([i for i in result_neg if i < 0]))
    print "-------------"
    print "accuracy of pos: ", accuracy_pos
    print "accuracy of neg: ", accuracy_neg
    print '\n'
    print "list of sorted set of pos: ", list(sorted(set(result_pos)))
    print "list of sorted set of neg: ", list(sorted(set(result_neg)))
    print '\n'
    self.io()
    return (accuracy_neg + accuracy_pos)/(len(result_neg) + len(result_pos))

  def io(self):
    """Input & Output"""
    pprint(self.resultant_dict)
    self.decouple_resultant_dict()
    self.resultant_pos_list.sort()
    self.resultant_neg_list.sort()
    self.write_dict_to_file(self.resultant_dict)
    self.write_list_to_file(self.resultant_pos_list)
    self.write_list_to_file(self.resultant_neg_list)

  def write_dict_to_file(self, arg):
    """VOID. Creates a file and writes the content of a dict to it."""
    name = 'resultant'
    with open('polarity-output_'+name+'.json', 'wb') as f:
      output = self.dict_to_json(arg)
      print >> f, output

  def write_list_to_file(self, arg):
    """VOID. Creates a file and writes the content of a list to it."""
    if arg == self.resultant_pos_list:
      name = 'resultant-pos'
    elif arg == self.resultant_neg_list:
      name = 'resultant-neg'
    else:
      name = 'ERROR'
    with open('polarity-output_'+name+'.out', 'wb') as f:
      for i in arg:
        print >> f, i

  def dict_to_json(self, dictionary):
    """Converts dictionary to a JSON format."""
    return dumps(dictionary, sort_keys=True, indent=4)

  def list_to_json(self, alist):
    """Converts list to a JSON format."""
    return dumps(alist, sort_keys=True, indent=0)

  def decouple_resultant_dict(self):
    """VOID. Decouples the resultant_dict into two separate dictionaries."""
    for k, v in self.resultant_dict.iteritems():
      if v > 0:
        self.resultant_pos_list.append(k)
      else:
        self.resultant_neg_list.append(k)

def main():
  pos_words = 'opinion-lexicon-English/positive-words.txt'
  # pos_words = raw_input("Please provide the path for positive words' lexicon:\n")
  print '\n'
  neg_words = 'opinion-lexicon-English/negative-words.txt'
  # neg_words = raw_input("Please provide the path for negative words' lexicon:\n")
  print '\n'
  corpus = 'sample.preprocessed.txt'
  # corpus = raw_input("Please finally provide the path for corpus:\n")
  instance = Polarity(pos_words, neg_words, corpus)
  from time import time, clock
  start = clock()
  val = instance.run()
  end = clock()
  measured = end - start
  print measured
  print val

if __name__ == '__main__':
    exit(main())