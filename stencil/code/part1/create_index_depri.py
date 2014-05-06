import argparse
import json 
import re
import porter_stemmer

# retrieve a list of postings containing a 
# business id, review id, and position of each term occurrence. 
# instead of using the review id, 
# use the line on which the review occurs in the yelp dataset file as a unique identifier
stopwords = []
term_map = {}
def create_index(data):
	idx = 0
	for line in data:
		line_json = json.loads(line)
		b_id = line_json['business_id']
		r_id = idx
		text = line_json['text'].split()
		for i in range(0, len(text)):	
			if text[i] in stopwords: 
				continue
			term = term_rp_process(text[i])
			if term =='': 
				continue
			if term in term_map:
				term_map[term].append((r_id,b_id,i))
			else:
				term_map[term] = [(r_id,b_id,i)]		

		idx += 1
		print idx
	return term_map

def term_rp_process(term):
	
	term = re.sub(r'[^\w\s]','',term)
	term = porter_stemmer.PorterStemmer().stem(term, 0,len(term)-1).encode('utf-8')
	return term.lower()


def load_stop_words():
	stop_words_file = open('./stopwords.txt')
	for ele in stop_words_file:
		stopwords.append(ele.strip('\n'))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', required=True, help='Path to input data')
	# parser.add_argument('-output', required=True, help='Path to output data')

	opts = parser.parse_args()

	load_stop_words()

	data = open(opts.input)
	create_index(data)

	data.close()
<<<<<<< HEAD:stencil/code/part1/create_index_depri.py


	with open('short_output.json', 'w') as outfile:
		json.dump(term_map, outfile)	

    # output = open(opts.output,'w')
=======
	with open('test_1.json', 'w') as outfile:
		json.dump(inv_idx, outfile)
	# output = open(opts.output,'w')
>>>>>>> b309d48b8bce4513f546be955b39c6431c6197a8:stencil/code/part1/create_index.py
	# for key in inv_idx:
	# 	output.write(str(key.encode('utf-8'))+":"+str(inv_idx[key])+"\n")
	# output.close()
if __name__ == '__main__':
	main()
