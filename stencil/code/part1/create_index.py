import argparse
import json 
import re
import porter_stemmer

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
			same_line = False
			for ele in term_map[term]:
				if ele['r_id'] == r_id:
					ele['idx'].append(i)
					same_line = True
			if not same_line:
				term_map[term].append({"r_id":r_id,"b_id": b_id,"idx": [i]})
		else:
			term_map[term] = [{"r_id":r_id,"b_id": b_id,"idx": [i]}]

def term_rp_process(term):
	
	term = re.sub(r'[^\w\s]','',term)
	term = re.sub('[^\x20-\x7E]*','',term)
	term = porter_stemmer.PorterStemmer().stem(term, 0,len(term)-1).encode('utf-8')
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
	# parser.add_argument('-output', required=True, help='Path to output data')

	opts = parser.parse_args()

	stopwords = load_stop_words()

	data = open(opts.input)
	inv_idx = create_index(data, stopwords)

	data.close()
	print json.dumps(inv_idx)
	# output = open(opts.output,'w')
	# for key in inv_idx:
	# 	output.write(str(key.encode('utf-8'))+":"+str(inv_idx[key])+"\n")
	# output.close()
if __name__ == '__main__':
	main()
