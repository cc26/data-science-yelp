from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import cross_validation
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from tokenizer import Tokenizer
from operator import itemgetter
import json

csv.field_size_limit(sys.maxsize)

def main():
	##### DO NOT MODIFY THESE OPTIONS ##########################
	parser = argparse.ArgumentParser()
	parser.add_argument('-training', required=True, help='Path to training data')
	parser.add_argument('-business_file', required=True, help='Path to business data')
	parser.add_argument('-c', '--classifier', default='nb', help='nb | log | svm')
	parser.add_argument('-top', type=int, help='Number of top features to show')
	parser.add_argument('-test', help='Path to test data')
	opts = parser.parse_args()
	############################################################

	##### BUILD TRAINING SET ###################################
	# Initialize CountVectorizer
	# You will need to implement functions in tokenizer.py
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)
	csv_file = open(opts.training)
	file_reader = csv.reader(csv_file)
	tweets = []
	lable = []
	for line in file_reader:
		tweets.append(line[2])
		lable.append(int(line[1]))
	vocabulary = vectorizer.fit_transform(tweets)
	#print tweets
	lable = np.array(lable)
	#print lable
	# Load training text and training labels
	# (make sure that your labels are converted to integers (0 or 1, not '0' or '1') 
	#  so that we can enforce the condition that label data is binary)

	# Get training features using vectorizer
	
	# Transform training labels to numpy array (numpy.array)
	
	############################################################
	
	##### TRAIN THE MODEL ######################################
	# Initialize the corresponding type of the classifier and train it (using 'fit')
	if opts.classifier == 'nb':
		classifier = BernoulliNB(binarize=None)
		classifier.fit(vocabulary, lable)
	elif opts.classifier == 'log':
		classifier = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None)
		classifier.fit(vocabulary, lable)
	elif opts.classifier == 'svm':
		classifier = LinearSVC(penalty='l2', loss='l2', dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None)
		classifier.fit(vocabulary, lable)
	else:
		raise Exception('Unrecognized classifier!')
	############################################################
	
	###### VALIDATE THE MODEL ##################################
	# Print training mean accuracy using 'score'
	print ("Training accuracy: %f" % classifier.score(vocabulary, lable))
	# Perform 10 fold cross validation (cross_validation.cross_val_score) with scoring='accuracy'
	# and print the mean score and std deviation
	scores = cross_validation.cross_val_score(classifier, vocabulary, lable, scoring = 'accuracy', cv=10)
	print("Cross-Validation Accuracy: %f (+/- %f)" % (scores.mean(), scores.std()))
	
	############################################################	

	##### EXAMINE THE MODEL ####################################
	if opts.top is not None:
		# print top n most informative features for positive and negative classes
		print 'Most informative features'
		util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
	############################################################
	

	##### TEST THE MODEL #######################################
	if opts.test is None:
		# Test the classifier on one sample test tweet
		# Tim Kraska 10:43 AM - 5 Feb 13
		test_tweet = 'Water dripping from 3rd to 1st floor while the firealarm makes it hard to hear anything. BTW this is the 2nd leakage.  Love our new house'
		
		terms = vectorizer.transform([test_tweet])

		# Print the predicted label of the test tweet
		print classifier.predict(terms)
		# Print the predicted probability of each label.
		if opts.classifier != 'svm':
			# Use predict_proba
			print classifier.predict_proba(terms)
		else:
			# Use decision_funcion
			print classifier.decision_function(terms)
	else:
		# Test the classifier on the given test set
		# Extract features from the test set and transform it using vectorizer
		csv_file = open(opts.test)
		file_reader = csv.reader(csv_file)
		test_tweets = []
		true_lable = []
		business = []
		for line in file_reader:
			business.append(line[0])
			test_tweets.append(line[2])
			true_lable.append(int(line[1]))
		terms = vectorizer.transform(test_tweets)
		true_lable = np.array(true_lable)
		predict_lable = classifier.predict(terms)
		# Print test mean accuracy
		accuracy = (len(true_lable) - sum(true_lable^predict_lable))/len(true_lable)
		print ("Test accuracy: %f" % accuracy)
		# Predict labels for the test set
		
		# Print the classification report
		target_names = ['Negative', 'Positive']

		if opts.classifier != 'svm':
			test_predicted_proba = classifier.predict_proba(terms)
			util.plot_roc_curve(true_lable, test_predicted_proba)

			positive_prob = []
			negative_prob = []
			for i, item in enumerate(true_lable):
				if true_lable[i] == 1:
					positive_prob.append([i, test_predicted_proba[i][0], test_predicted_proba[i][1]])
				else:
					negative_prob.append([i, test_predicted_proba[i][0], test_predicted_proba[i][1]])
			sorted_positive = sorted(positive_prob, key=itemgetter(1), reverse= True)
			positive_bias = sorted_positive[0:5]
			sorted_negative = sorted(negative_prob, key=itemgetter(1))
			negative_bias = sorted_negative[0:5]

			bfile = open(opts.business_file, 'r')
			bdic = {}
			for line in bfile:
				line = json.loads(line)
				bdic[line['business_id']] = line['name']
			print '\n'
			print 'top 5 positively biased businesses are:'
			for item in positive_bias:
				print bdic[business[item[0]]]
			print '\n'
			print 'top 5 negatively biased businesses are:'
			for item in negative_bias:
				print bdic[business[item[0]]]

		'''
		print 'Classification Report:'
		print classification_report(true_lable, predict_lable, target_names=target_names)
		# Print the confusion matrix
		print 'Confusion Matrix:'
		print confusion_matrix(true_lable, predict_lable)
		
		# Get predicted label of the test set
		if opts.classifier != 'svm':
			# Use predict_proba
			test_predicted_proba = classifier.predict_proba(terms)
			print 'Prediction Probabilities:'
			print test_predicted_proba
			# Plot ROC curve
			util.plot_roc_curve(true_lable, test_predicted_proba)
			i = 0
			index = {}
			max_prob = []
			for item in test_predicted_proba:
				max_prob.append(max(item))
				index[max(item)] = i
				i+=1
			sorted_max = sorted(max_prob, reverse = True)
			correct = 0
			correct_tweet = []
			incorrect = 0
			incorrect_tweet = []
			for value in sorted_max:
				if (true_lable[index[value]] == predict_lable[index[value]]) and correct < 5:
					correct_tweet.append((test_tweets[index[value]], max_prob[index[value]]))
					correct+=1
				if (true_lable[index[value]] != predict_lable[index[value]]) and incorrect < 5:
					incorrect_tweet.append((test_tweets[index[value]], max_prob[index[value]]))
					incorrect+=1
			#5 tweets with highest predicted probabilities that are correctly classified
			print 'Correct Tweets:'
			print correct_tweet
			print "\n"
			#5 tweets with highest predicted probabilities that are incorrectly classified
			print 'Incorrect Tweets:'
			print incorrect_tweet
			
		else:
			# Use decision_funcion
			print 'Decision_Function:'
			print classifier.decision_function(terms)
			
	############################################################'''


 		
if __name__ == '__main__':
	main()
