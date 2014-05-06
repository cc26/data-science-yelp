from porter_stemmer import PorterStemmer
import re
import string

class Tokenizer(object):
	def __init__(self):
		self.stemmer = PorterStemmer()

	def process_review(self, tweet):
		#TODO: pre-process tweet
		# this is a helper function for __call__
		
		tweet = tweet.lower() # To lower case
		tweet = re.sub('[^\x20-\x7E]*','',tweet)
		tweet = re.sub(r'([a-z0-9])\1+',r'\1\1',tweet) #Replace two or more occurrences of the same character with two occurrences

		stopword_file= open("stopwords.txt")
		stopwords =set()
		stopword_content = stopword_file.readlines()
		for word in stopword_content:
			stopwords.add(word.strip().lower())


		tweet_words = tweet.split(" ")
		tweet = ""
		for w in tweet_words:
			if len(w)< 1 or w in stopwords:
				continue
			elif not w[0].isalpha(): 
				continue
			else:
				tweet+= " "+w
		tweet = ''.join(ch for ch in tweet if ch not in string.punctuation)

		tweet_words = [self.stemmer.stem(word, 0, len(word)-1) for word in tweet.split(" ")]

		return tweet_words

	def __call__(self, doc):
		# this function will tokenize the given document and return a list of extracted features (tokens)
		processed_doc = self.process_tweet(doc)
		#TODO: return a list of features extracted from processed_doc
		return processed_doc
