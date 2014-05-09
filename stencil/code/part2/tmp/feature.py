import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-business_file', required=True, help='Path to business data')
	opts = parser.parse_args()
	# f_reviews = open(opts.review_file,'r')
	f_business = open(opts.business_file,'r')
	count = 0
	total = 0
        t = 0
	f = 0

	for line in f_business:
		line = json.loads(line)
		if line['review_count'] >= 10 and line['stars'] >= 4:
			count += 1
			if 'Price Range' in line['attributes']:
				total += 1
                                print line['attributes']['Price Range']

	print 'Total group ' + str(total)
        print 'True is ' + str(t)
	print 'False is '+ str(f)

if __name__ == '__main__':
	main()
