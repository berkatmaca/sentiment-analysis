#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division

class Evaluation(object):
  def __init__(self, gold_polarity, predicted_polarity):
    self.gold_polarity = gold_polarity
    self.predicted_polarity = predicted_polarity
    self.accuracy = float()

  def get_accuracy(self):
  	return self.accuracy

  def count_accuracy(self):
  	total_num_files = len(self.gold_polarity)
  	#print total_num_files
  	correct_prediction = set(self.gold_polarity.items()) & set(self.predicted_polarity.items())
  	num_correct_pred = len(correct_prediction)
  	#print num_correct_pred
  	self.accuracy = num_correct_pred / total_num_files
  	return self.accuracy
