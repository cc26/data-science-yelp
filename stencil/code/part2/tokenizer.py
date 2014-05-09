from porter_stemmer import PorterStemmer
import re

class Tokenizer(object):
	def __init__(self):
		self.stemmer = PorterStemmer()

	def __call__(self, tweet):
		
		# TODO: This function takes in a single tweet (just the text part)
		# then it will process/clean the tweet and return a list of tokens (words).
		# For example, if tweet was 'I eat', the function returns ['i', 'eat']
		# Lowercase the tweet and strip punctuations
		parsed = tweet.lower().replace(',',' ').replace('.',' ').replace('?',' ').replace('!',' ').replace('-',' ').replace('#',' ').replace(':',' ').replace('(',' ').replace(')',' ').replace('=',' ').replace('...',' ').split()
		for i, word in enumerate(parsed):
			# do replacement
			if '@' in word:
				parsed[i] = 'AT_USER'
			if ('www.' in word) or ('.com' in word) or ('http://' in word) or ('http(s)://' in word):
				parsed[i] = 'URL'
			# Replacing three or more occurrence of the same character with one occurrence using regular expression
			parsed[i] = re.sub(r'(.)\1{2,}', r'\1', parsed[i])
		# Apply stemming to each term to restore its original form
		res = [self.stemmer.stem(kw, 0, len(kw)-1) for kw in parsed]
		# De-duplicate the term list to make it only contains distinct terms
		res = list(set(res))
		# You will not need to call this function explictly. 
		# Once you initialize your vectorizer with this tokenizer, 
		# then 'vectorizer.fit_transform()' will implictly call this function to 
		# extract features from the training set, which is a list of tweet texts.
		# So once you call 'fit_transform()', the '__call__' function will be applied 
		# on each tweet text in the training set (a list of tweet texts),

		return res
