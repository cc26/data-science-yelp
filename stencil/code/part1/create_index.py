import argparse
import json
from tokenizer import Tokenizer

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-review_file', required=True, help='Path to review data')
	parser.add_argument('-business_file', required=True, help='Path to business data')
	parser.add_argument('-output', required=True, help='Path to output index file')
	opts = parser.parse_args()
	f_reviews = open(opts.review_file,'r')
	f_business = open(opts.business_file,'r')

	line_num = 0
	b_map = {}
	for line in f_business:
		b_obj = json.loads(line)
		b_map[b_obj['business_id']] = line_num
		line_num += 1

	tokenizer = Tokenizer()
	wordsmap = {}
	line_num = 0
	for line in f_reviews:
		r = json.loads(line)
		words = tokenizer.process_review(r['text']);
		w_idx = 0
		for w in words:
			if w=="":
				continue
			b_id = b_map[r['business_id']]
			if w in wordsmap:
				if b_id in wordsmap:
					b_map = wordsmap[w][b_id]
					if line_num in b_map:
						b_map[line_num].append(w_idx)
					else:
						b_map[line_num] = [w_idx]
				else:
					wordsmap[w][b_id] = {line_num:[w_idx]}
			else:
				wordsmap[w] = {b_id:{line_num:[w_idx]}}
			w_idx += 1
		line_num += 1
		if line_num % 1000==0:
			print line_num 
		# if line_num == 1000:
		# 	break
		
	with open(opts.output, 'w') as f_out:
		json.dump(wordsmap, f_out)
		# print "total:" + str(len(wordsmap))
		# count = 0
		# for k,v in wordsmap.items():
		# 	json.dump({k:v}, f_out)
		# 	f_out.write('\n')
		# 	count +=1
		# 	if count % 1000 == 0:
		# 		print count


if __name__ == '__main__':
	main()
