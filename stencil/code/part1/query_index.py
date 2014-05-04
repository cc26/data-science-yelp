import sys
import argparse
import json

inverted_index = {}

def one_word_query(line):
	print"one_word_query:",line



def free_text_query(line):
	print "free_text_query:",line
def phrase_query(line):
	print "phrase_query:",line

def load_file(data):

	print "loading file"

	for line in data:
		inverted_index[line] = data[line]
	
	print "finish loading data"

def main():
	# first read in the inverted index file
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', required=True, help='Path to inverted_index')

	opts = parser.parse_args()
	data = open(opts.input)
	load_file(json.load(data))
	data.close()

	# TODO: need to check error input  
	for line in sys.stdin:
		f_type = len(line.split())
		if f_type == 1:
			one_word_query(line)
		else:
			if line[0] == '"':
				phrase_query(line)
			else:
				free_text_query(line)
if __name__ == '__main__':
	main()

