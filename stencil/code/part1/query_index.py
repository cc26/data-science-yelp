import sys
import argparse
import json
from sets import Set
inverted_index = {}

def one_word_query(line):
	print"one_word_query:",line

	if line not in inverted_index:
		print "term not found"
		return []
	result = Set()
	list_values = inverted_index[line]
	for ele in list_values:
		result.add(ele['b_id'])

	result = list(result)

	print result
	return result


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
		line = line.strip('\n')
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

