#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Review import Review 
from Evaluation import Evaluation
import os

pos_lex = raw_input("Please provide the path for positive words' lexicon:\n")
print '\n'
neg_lex = raw_input("Please provide the path for negative words' lexicon:\n")
print '\n'
pos_reviews = raw_input("Please provide the path for the directory with positive reviews:\n")
neg_reviews = raw_input("Please provide the path for the directory with negative reviews:\n")
path = [pos_reviews, neg_reviews]
# path = ["/home/maria/Documents/UNI_Stuttgart/2_semester/Sentiment_Analysis/project/txt_sentoken/pos", "/home/maria/Documents/UNI_Stuttgart/2_semester/Sentiment_Analysis/project/txt_sentoken/neg"]
dict_gold = dict()
dict_pred = dict()

for i in path:
	for filename in os.listdir(i):
		rew = Review(i + "/" + filename)
		
		polarity = rew.predict_polarity(pos_lex, neg_lex)
		if rew.filename in dict_gold:
			print "This file name already exist."
		else:
			dict_gold[rew.filename] = rew.get_polarity_gold()
			dict_pred[rew.filename] = rew.polarity_predict
evaluator = Evaluation(dict_gold, dict_pred)
evaluator.count_accuracy()
print evaluator.get_accuracy()
		# print "predicted polarity: ", polarity
		# print "gold polarity: ", rew.get_polarity_gold()
		# print rew.filename
		# print "pos --> ", rew.num_pos_terms
		# print "neg --> ", rew.num_neg_terms
