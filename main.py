#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Review import Review 
from Evaluation import Evaluation
import os
""" Here one of the two methods, Score based or Valence based, can be executed. 
So running this program reviews polarity is predicted and the applied method is evaluated."""

pos_lex = raw_input("Please provide the path for positive words' lexicon:\n")
print '\n'
neg_lex = raw_input("Please provide the path for negative words' lexicon:\n")
print '\n'
pos_reviews = raw_input("Please provide the path for the directory with positive reviews:\n")
print '\n'
neg_reviews = raw_input("Please provide the path for the directory with negative reviews:\n")
print '\n'
write_pos_reviews = raw_input("Please provide the path for the directory to write positive reviews into:\n")
print '\n'
write_neg_reviews = raw_input("Please provide the path for the directory to write negative reviews into:\n")
print '\n'


path = [pos_reviews, neg_reviews]
method = raw_input("Choose one of the methods: ScoreBased or ValenceBased. Type in one of the methods' names:\n")
dict_gold = dict()
dict_pred = dict()

for i in path:
	for filename in os.listdir(i):
		rew = Review(i + "/" + filename)
		
		
		if method == "ScoreBased":
			""" The line below calls the Score based method."""
			polarity = rew.predict_polarity_scoreBased(pos_lex, neg_lex)
		elif method == "ValenceBased":
			""" The line below calls the Valence based method."""
			polarity = rew.predict_polarity_valenceBased(pos_lex, neg_lex)
		else: 
			print '\n'
			print "Wrong input. Check spelling."
			print '\n'
		if rew.filename in dict_gold:
			print "This file name already exist."
		else:
			dict_gold[rew.filename] = rew.get_polarity_gold()
			dict_pred[rew.filename] = polarity

		""" Write into the folders predicted positive reviews and predicted negative reviews. 
		Please, provide your own paths."""
		if rew.polarity_predict == "pos":
			""" Please, provide path for positive reviews."""
			with open(write_pos_reviews +"/"+ rew.filename, "w+") as f:
				f.write(" ".join(rew.get_wordsList()))
		if rew.polarity_predict == "neg":
			""" Please, provide path for negative reviews."""
			with open(write_neg_reviews +"/"+ rew.filename, "w+") as f:
				f.write(" ".join(rew.get_wordsList()))

evaluator = Evaluation(dict_gold, dict_pred)
evaluator.count_accuracy()
if method == "ScoreBased" :
	print "Accuracy of the score based method is ", evaluator.get_accuracy()
elif method == "ValenceBased" :
	print "Accuracy of the valence based method is ", evaluator.get_accuracy()
