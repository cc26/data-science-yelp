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
	words = line.split()
	result = []
	for ele in inverted_index[words[0]]:
		if ele['b_id'] not in result:
			result.append(ele['b_id'])
	for word in words[1:len(words)]:
		if len(result) == 0: break
		tmp = inverted_index[word]
		rem = []
		for i, bid in enumerate(result):
			flag = 0
			for term in tmp:
				if bid == term['b_id']:
					flag = 1
					break
			if flag == 0: rem.append(result[i])
		for ele in rem:
			result.remove(ele)
        print result
	return result

def phrase_query(line):
	line = line.strip('"')
	words = line.split()
	result = []
	business = []
	for ele in inverted_index[words[0]]:
		if ele['b_id'] not in business:
			business.append(ele['b_id'])
			result.append(ele)
	for word in words[1:len(words)]:
		if len(result) == 0: break
		tmp = inverted_index[word]
		rem = []
		for i, dic in enumerate(result):
			flag = 0
			for term in tmp:
				if (dic['b_id'] == term['b_id'] and dic['r_id'] <= term['r_id'] and dic['idx'] <= term['idx']):
					result[i] = term
					flag = 1
					break
			if flag == 0: rem.append(result[i])
		for ele in rem:
			result.remove(ele)
			business.remove(ele['b_id'])
	print business
	return business

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

