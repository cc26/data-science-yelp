import argparse
import json 
import re
# retrieve a list of postings containing a 
# business id, review id, and position of each term occurrence. 
# instead of using the review id, 
# use the line on which the review occurs in the yelp dataset file as a unique identifier


def create_index(data, stop_words):

	idx = 0
	term_map = {}
	for line in data:
		line_json = json.loads(line)
		create_entry(line_json, idx, term_map, stop_words)
		idx += 1
		if idx == 1000:
			break
	return term_map

def create_entry(line, line_number, term_map, stop_words):
	entry = {}
	b_id = line['business_id']
	r_id = line_number
	text = line['text'].split()
	for i in range(0, len(text)):	
		term = term_rp_process(text[i])
		if term in stop_words: 
			continue
		if term =='': 
			continue
		if term in term_map:
			term_map[term] += (r_id, b_id, i)
		else:
			term_map[term] = [(r_id, b_id, i)]

def term_rp_process(term):
	
	term = re.sub(r'[^\w\s]','',term)
	term = re.sub('[^\x20-\x7E]*','',term)
	return term.lower()


def load_stop_words():
	stop_words_file = open('./stopwords.txt')
	stop_words = []
	for ele in stop_words_file:
		stop_words += [ele.strip('\n')]
	return stop_words

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', required=True, help='Path to input data')
	parser.add_argument('-output', required=True, help='Path to output data')

	opts = parser.parse_args()

	stopwords = load_stop_words()
	print stopwords
	data = open(opts.input)
	inv_idx = create_index(data, stopwords)

	data.close()

	output = open(opts.output,'w')
	for key in inv_idx:
		output.write(str(key.encode('utf-8'))+" "+str(inv_idx[key])+"\n")
	output.close()
if __name__ == '__main__':
	main()
