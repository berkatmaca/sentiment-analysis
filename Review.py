#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Lexicon import Lexicon
import random 
import re

class Review(object):
  def __init__(self, review_path):
    self.review_path = review_path
    self.wordsList = self.read_review()
    self.filename = self.get_filename()
    self.num_neg_terms = 0
    self.num_pos_terms = 0
    self.polarity_gold = self.set_gold_polarity()
    self.polarity_predict = str()

  def get_wordsList(self):
    return self.wordsList

  def read_review(self):
    lines = str()
    with open(self.review_path) as f:
      for line in f:
        lines += line
      self.wordsList = lines.split()
    return self.wordsList

  def get_filename(self):
    self.filename = re.split("/", self.review_path)[-1]
    return self.filename

  def set_gold_polarity(self):
    # self.polarity_gold = str()
    if re.search("/pos/", self.review_path):
      self.polarity_gold = "pos"
    elif re.search("/neg/", self.review_path):
      self.polarity_gold = "neg"
    else:
      print "You did not specify in the path if the review is pos or neg. Please, check your path. OR You don't know the gold_polarity."
    return self.polarity_gold

  def get_polarity_gold(self):
    return self.polarity_gold


  def predict_polarity(self, pos_lex, neg_lex):
    score = 0
    lexicon = Lexicon(pos_lex, neg_lex)
    #lexicon = Lexicon("/home/maria/Documents/UNI_Stuttgart/2_semester/Sentiment_Analysis/project/opinion-lexicon-English/positive-words.txt","/home/maria/Documents/UNI_Stuttgart/2_semester/Sentiment_Analysis/project/opinion-lexicon-English/negative-words.txt")
    for word in self.wordsList:
      if word in lexicon.get_pos_terms():
        self.num_pos_terms += 1
        #print word
      if word in lexicon.get_neg_terms():
        self.num_neg_terms += 1
    score = self.num_pos_terms - self.num_neg_terms
    if score > 0:
      self.polarity_predict = "pos"
    elif score < 0:
      self.polarity_predict = "neg"
    else:
      self.polarity_predict = random.choice(["pos", "neg"])
    return self.polarity_predict