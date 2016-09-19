#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import exit
from json import dumps
from math import log10
from pprint import pprint

class Polarity:
  """Estimates each word's polarity using Turney's extended metric of PMI."""
  def __init__(self, pos_words_path, neg_words_path, corpus_path, window=5):
    self.pos_words_path = pos_words_path
    self.neg_words_path = neg_words_path
    self.corpus_path = corpus_path
    self.window = window
    self.pos_word_list = self.retrieve_words(pos_words_path)
    self.neg_word_list = self.retrieve_words(neg_words_path)
    self.corpus_word_dict = dict() # UNSETTLED!
    self.corpus_word_list = list()
    self.tolerance = 0.01
    self.retrieve_corpus()
    self.resultant = dict()
    self.resultant_pos = list()
    self.resultant_neg = list()
    self.indices_of_excellent = self.get_indices('excellent')
    self.indices_of_poor = self.get_indices('poor')
    self.window_for_excellent = self.create_window(self.indices_of_excellent)
    self.window_for_poor = self.create_window(self.indices_of_poor)

  def get_pos_word_list(self):
    return self.pos_word_list

  def get_neg_word_list(self):
    return self.neg_word_list

  def get_corpus_word_list(self):
    return self.corpus_word_list

  "@UNSETTLED"
  # def get_corpus_word_dict(self):
  #   return self.corpus_word_dict

  def get_tolerance(self):
    return self.tolerance

  def get_window(self):
    return self.window

  def get_resultant(self):
    return self.resultant

  def get_resultant_pos(self):
    return self.resultant_pos

  def get_resultant_neg(self):
    return self.resultant_neg

  def set_tolerance(self, new_tolerance):
    self.tolerance = new_tolerance

  def set_window(self, new_window):
    self.window = new_window

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

  def hits(self, of_word):
    """Returns a floating-point number that represents the
    occurrence of a given word in the corpus (+ tolerance value)."""
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
    freq_total = self.corpus_word_list.count(of_word)
    return freq_total + self.tolerance

  def hits_nearing(self, nearing_word, keyword):
    """Returns a floating-point number that represents
    the co-occurrence of a word and the keyword
    (+ tolerance value)."""
    hit = int()
    if keyword == 'excellent':
      hit += self.window_for_excellent.count(nearing_word)
    elif keyword == 'poor':
      hit += self.window_for_poor.count(nearing_word)
    return hit + self.tolerance

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
    """Consumes a list of integers that represents indices of
    a given word (either 'excellent' or 'poor', in this case)
    occurring in the corpus and returns a list of strings that
    are window-value-away (both to the left and right) to the
    word situated on that index."""
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
    ctrl = 0 # Represents positive=0 and negative=-1.
    result_pos, result_neg = list(), list()
    pos_neg = [self.pos_word_list, self.neg_word_list]
    for word_list in pos_neg:
      if ctrl == 0:
        for word in word_list:
          eval_SO = self.evaluate_semantic_orientation(word)
          self.resultant[word] = eval_SO
          result_pos.append(eval_SO)
      else:
        for word in word_list:
          eval_SO = self.evaluate_semantic_orientation(word)
          self.resultant[word] = eval_SO
          result_neg.append(eval_SO)
      ctrl = -1
    accuracy_pos = float(len([i for i in result_pos if i > 0]))/len(result_pos)
    accuracy_neg = float(len([i for i in result_neg if i < 0]))/len(result_neg)
    print "-------------"
    print "accuracy of pos: ", accuracy_pos
    print "accuracy of neg: ", accuracy_neg
    print '\n'
    print "list of sorted set of pos: ", list(sorted(set(result_pos)))
    print "list of sorted set of neg: ", list(sorted(set(result_neg)))
    print '\n'
    pprint(self.resultant)
    self.decouple_resultant()
    self.resultant_pos.sort()
    self.resultant_neg.sort()
    self.write_dict_to_file(self.resultant)
    self.write_list_to_file(self.resultant_pos)
    self.write_list_to_file(self.resultant_neg)
    return (accuracy_neg + accuracy_pos)/2

  def write_dict_to_file(self, arg):
    """VOID. Creates a file and writes the content of a dict to it."""
    name = 'resultant'
    with open('polarity-output_'+name+'.json', 'wb') as f:
      output = self.dict_to_json(arg)
      print >> f, output

  def write_list_to_file(self, arg):
    """VOID. Creates a file and writes the content of a list to it."""
    name = str()
    if arg == self.resultant_pos:
      name = 'resultant-pos'
    elif arg == self.resultant_neg:
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

  def decouple_resultant(self):
    """VOID. Decouples the resultant into two separate dictionaries."""
    for k, v in self.resultant.iteritems():
      if v > 0:
        self.resultant_pos.append(k)
      else:
        self.resultant_neg.append(k)

def main():
  pos_words = '/home/atmaca/Documents/ims/courses/ss16/sentiment-analysis/mini-projects/2/opinion-lexicon-English/positive-words.txt'# raw_input("Please provide the path for positive words' lexicon:\n")
  print '\n'
  neg_words = '/home/atmaca/Documents/ims/courses/ss16/sentiment-analysis/mini-projects/2/opinion-lexicon-English/negative-words.txt'# raw_input("Please provide the path for negative words' lexicon:\n")
  print '\n'
  corpus = 'sample.preprocessed.txt'# raw_input("Please finally provide the path for corpus:\n")
  instance = Polarity(pos_words, neg_words, corpus)
  print instance.run()

if __name__ == '__main__':
    exit(main())