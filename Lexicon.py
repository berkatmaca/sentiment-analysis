#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Lexicon(object):
  def __init__(self, pos_terms_path, neg_terms_path):
    self.pos_terms_path = pos_terms_path
    self.neg_terms_path = neg_terms_path
    self.pos_terms = self.retrieve_words(pos_terms_path)
    self.neg_terms = self.retrieve_words(neg_terms_path)

  def get_pos_terms(self):
    return self.pos_terms

  def get_neg_terms(self):
    return self.neg_terms

  def retrieve_words(self, filename):
    words_list = list()
    with open(filename, 'r') as f:
      for line in f:
        line = line.strip()
        words_list.append(line)
    return words_list