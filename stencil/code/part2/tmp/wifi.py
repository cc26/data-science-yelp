import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-business_file', required=True, help='Path to business data')
	opts = parser.parse_args()
	# f_reviews = open(opts.review_file,'r')
	f_business = open(opts.business_file,'r')
	count = 0
	wifi = 0
	paid = 0
	free = 0
	no = 0
	for line in f_business:
		line = json.loads(line)
		if line['review_count'] >= 10 and line['stars'] >= 4:
			count += 1
			if 'Wi-Fi' in line['attributes']:
				wifi += 1
				if line['attributes']['Wi-Fi'] == 'no':
					no += 1
				elif line['attributes']['Wi-Fi'] == 'free':
					free += 1
				elif line['attributes']['Wi-Fi'] == 'paid':
					paid += 1
	print 'Total wifi ' + str(wifi)
	print 'No wifi ' + str(no)
	print 'Paid wifi ' + str(paid)
	print 'Free wifi ' + str(free)

if __name__ == '__main__':
	main()