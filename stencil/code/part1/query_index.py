import sys
import argparse
import json
from sets import Set
from math import log
from tokenizer import Tokenizer

def one_word_query(word, wordsmap):
	if word not in wordsmap:
		print "term not found"
		return []
	return list(wordsmap[word].keys())


def free_text_query(words, wordsmap):
	result = set()
	isFirstSet = True
	for w in words:
		curSet = set(wordsmap[w].keys())
		if isFirstSet:
			result = curSet
			isFirstSet = False
		else:
			result = result.intersection(curSet)
	return result

def phrase_query(words, wordsmap):
	# process the first word
	cur_map = {}
	first = words[0]
	b_dicts = wordsmap[first]
	for b_id in b_dicts.keys():
		r_dicts = b_dicts[b_id]
		for r_id in r_dicts.keys():
			cur_map[r_id] = (r_dicts[r_id][0], b_id)
	for word in words[1:]:
		b_dicts = wordsmap[word]
		new_map = {}
		for b_id in b_dicts.keys():
			r_dicts = b_dicts[b_id]
			for r_id in r_dicts.keys():
				if r_id in cur_map:
					pos, _ = cur_map[r_id] 
					for cur_pos in r_dicts[r_id]:
						if cur_pos > pos:
							new_map[r_id] = (cur_pos, b_id)
							break
		cur_map = new_map
	result = []
	for k in cur_map.keys():
		_, b_id = cur_map[k]
		result.append(b_id)
	return result

def get_tf_idf(term, b_id,wordsmap):
	reviews = wordsmap[term][b_id]
	tf = 0
	for r in reviews.values():
		tf += len(r)
	N = 15585
	idf = log(N) - log(len(wordsmap[term].keys()))
	return tf*idf


def rank(words,businesses,b_map,wordsmap):
	scores = []
	for b_id in businesses:
		score = 0
		for w in words:
			score += get_tf_idf(w, b_id,wordsmap)
		score *= log(int(b_map[b_id]['review_count'])) * float(b_map[b_id]['stars'])
		scores.append((b_id, score))
	scores.sort(key=lambda x:-x[1])
	result = [b_map[k]['business_id'] for (k,_) in scores]
	if len(result) <=10:
		return result
	else:
		return result[:10]

def main():
	# first read in the inverted index file
	parser = argparse.ArgumentParser()
	parser.add_argument('-index', required=True, help='Path to inverted index file')
	parser.add_argument('-business', required=False, help='Path to yelp business data json file', default="/course/cs1951a/pub/final/data/extracted/yelp_academic_dataset_business.json")
	opts = parser.parse_args()

	# Pre-processing
	f_index = open(opts.index,'r')
	print "loading index file..."
	wordsmap = {}
	# count = 0
	# for line in f_index:
	# 	count += 1
	# 	j_obj = json.load(line)
	# 	for k, v in j_obj.items():
	# 		wordsmap[k] = v
	# 	j_obj = None
	# 	if count % 100 == 0:
	# 		print count
	wordsmap = json.load(f_index)
	print "done"
	f_index.close()
	b_map = {}
	print "loading business file..."
	f_b = open(opts.business, 'r')
	line_num = 0
	for line in f_b:
		b_json = json.loads(line)
		b_map[str(line_num)]={"business_id":b_json['business_id'],"review_count":int(b_json['review_count']), "stars":float(b_json['stars'])}
		line_num += 1
	print "done"


	tokenizer = Tokenizer()
	# TODO: need to check error input  
	# Bug: c-d exit situation
	
	for line in sys.stdin:
		result = []
		line = line.strip('\n')
		if len(line)==0:
			continue
		elif line[0]=='"':
			line = line.strip('"')
			words = tokenizer.process_review(line)
			result = phrase_query(words, wordsmap)
		elif len(line.split())==1:
			words = tokenizer.process_review(line)
			result = one_word_query(words[0], wordsmap)
		else:
			words = tokenizer.process_review(line)
			result = free_text_query(words, wordsmap)
		rank_res = rank(words,result,b_map,wordsmap)
		print rank_res
	

if __name__ == '__main__':
	main()

