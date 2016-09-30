#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Lexicon import Lexicon
import random 
import re

class Review(object):
  """ Contains the info about review: text, aount of positive and negative words,
  its gold and predicted polarity."""
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
    """ Retrieves gold polarity from the provided path to the review file.
    So in order to retrieve it, there should be "pos" or "neg" folder in the path."""
    if re.search("/pos", self.review_path):
      self.polarity_gold = "pos"
    elif re.search("/neg", self.review_path):
      self.polarity_gold = "neg"
    else:
      print "You did not specify in the path if the review is pos or neg. Please, check your path. OR You don't know the gold_polarity."
    return self.polarity_gold

  def get_polarity_gold(self):
    return self.polarity_gold


  def predict_polarity_scoreBased(self, pos_lex, neg_lex):
    """ The first method to predict review's polarity. It predicts polarity according to the review's general score. 
    A token of the review is matched to a polarity lexicon. If the token is matched with the positive term, number
    of positive words of the review increments, if the token has a match with the negative term, number of negative
    words is incremented. And the total score of the review is the difference in the amount of positive and negative
    words. If score is positive than the perdicted polarity of the review is positive, if negative than the perdicted
    polarity is negative. """
    score = 0
    lexicon = Lexicon(pos_lex, neg_lex)
    for word in self.wordsList:
      if word in lexicon.get_pos_terms():
        self.num_pos_terms += 1
      elif word in lexicon.get_neg_terms():
        self.num_neg_terms += 1
    score = self.num_pos_terms - self.num_neg_terms
    if score > 0:
      self.polarity_predict = "pos"
    elif score < 0:
      self.polarity_predict = "neg"
    else:
      self.polarity_predict = random.choice(["pos", "neg"])
    return self.polarity_predict

  def predict_polarity_valenceBased(self, pos_lex, neg_lex):
    """ The first method to predict review's polarity. It predicts polarity according to the general valence review receives at the end.
    valence of positive term is +2 and negative - -2. But there are negations, downtoners and amplifiers that change it. Negations: 
    negation + pos = -2; negation + neg = +2. Downtoners: downtoner + pos = +1; downtoner + neg = -1. Amplifiers: amplifier + pos = +3;
    amplifier + neg = -3. They all are added to the general valence of the review. so if valence is positive, the review if rendered positive,
    if negative, than review is negative. """

    negations = ["not", "never", "none", "nobody", "nowhere", "nothing", "neither", "don't", "doesn't",
                 "didn't", "isn't", "aren't", "wasn't", "weren't", "won't", "wouldn't", "shouldn't"]
    downtoners = ["rather", "quite", "pretty", "fairly", "somewhat", "simply", "almost", "barely",
                  "hardly", "nearly", "relatively", "practically"]
    amplifiers = ["deeply", "absolutely", "strongly", "amazingly", "so", "extremely", "very", "really",
                  "too", "absolutely", "incredibly", "insanely", "awfully", "dreadfully", "terribly",
                  "downwright", "entirely", "highly", "irretrievably", "perfectly", "sharply", 
                  "strikingly", "totally", "surely", "unbelievably", "completely", "sure", "that", 
                  "frankly", "suprisingly", "unnaturally", "unusually"]
    valence = 0
    lexicon = Lexicon(pos_lex, neg_lex)
    for i in range(len(self.wordsList)):
      if self.wordsList[i] in lexicon.get_pos_terms():
        if (self.wordsList[i-1] in negations) or (self.wordsList[i-2] in negations): # 2 words before the target word (polarity term)
          valence += -2
        if (self.wordsList[i-1] in downtoners) or (self.wordsList[i-2] in downtoners):
          valence += 1
        if (self.wordsList[i-1] in amplifiers) or (self.wordsList[i-2] in amplifiers):
          valence += 3
        else:
          valence += 2
      if self.wordsList[i] in lexicon.get_neg_terms():
        if (self.wordsList[i-1] in negations) or (self.wordsList[i-2] in negations): 
          valence += 2
        if (self.wordsList[i-1] in downtoners) or (self.wordsList[i-2] in downtoners):
          valence += -1
        if (self.wordsList[i-1] in amplifiers) or (self.wordsList[i-2] in amplifiers):
          valence += -3
        else:
          valence += -2
    # print valence
    if valence > 0:
      self.polarity_predict = "pos"
    elif valence < 0:
      self.polarity_predict = "neg"
    else:
      self.polarity_predict = random.choice(["pos", "neg"])
    return self.polarity_predict

        


    