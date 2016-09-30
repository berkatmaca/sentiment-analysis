#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division

class Evaluation(object):
  """ This class gives the accurasy of the polarity classifier. It takes two dictionaries, one with a file name and its gold polarity,
  the second with a file name and its predicted polarity. Comparing this two the accuracy is computed."""
  def __init__(self, gold_polarity, predicted_polarity):
    self.gold_polarity = gold_polarity
    self.predicted_polarity = predicted_polarity
    self.accuracy = float()

  def get_accuracy(self):
  	return self.accuracy

  def count_accuracy(self):
    total_num_files = len(self.gold_polarity)
    gold_pol = set(self.gold_polarity.items())
    pred_pol = set(self.predicted_polarity.items())
    """ Correctly classified (Treu positive)"""
    correct_prediction = gold_pol & pred_pol 
    """ Wrongly classified, should have been the class in gold (True negative)"""
    correct_prediction_gold = list(gold_pol.difference(pred_pol)) 
    """ Wrongly classified into the predicted class (False positive)"""
    incorrect_prediction_pred = list(pred_pol.difference(gold_pol)) 
    num_correct_pred = len(correct_prediction)
    # print num_correct_pred
    self.accuracy = num_correct_pred / total_num_files
    return self.accuracy
