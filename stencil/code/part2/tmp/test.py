import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-business_file', required=True, help='Path to business data')
	opts = parser.parse_args()
	# f_reviews = open(opts.review_file,'r')
	f_train = open('train.txt', 'w')
	f_test = open('test.txt', 'w')
	f_business = open(opts.business_file,'r')
	tot1 = 0
	tot2 = 0
	count1 = 0
	count2 = 0
	for line in f_business:
		line = json.loads(line)
		if line['review_count'] >= 5:
			tot1 += 1
			if line['stars'] >= 4.5:
				f_train.write(str(line['business_id'])+' '+'1'+'\n')
				count1 += 1
			else:
				f_train.write(str(line['business_id'])+' '+'0'+'\n')
		else:
			tot2 += 1
			if line['stars'] >= 4.5:
				f_test.write(str(line['business_id'])+' '+'1'+'\n')
				count2 += 1
			else:
				f_test.write(str(line['business_id'])+' '+'0'+'\n')
	
	f_train.flush()
	f_train.close()
	f_test.flush()
	f_test.close()
	print tot1
	print count1
	print tot2
	print count2

if __name__ == '__main__':
	main()
