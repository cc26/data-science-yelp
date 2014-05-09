import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-business_file', required=True, help='Path to business data')
	opts = parser.parse_args()
	# f_reviews = open(opts.review_file,'r')
	f_business = open(opts.business_file, 'r')
	count = 0
	for line in f_business:
		line = json.loads(line)
		if line['name'] == "McDonald's":
			print line['review_count']
	

if __name__ == '__main__':
	main()
