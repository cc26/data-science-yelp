import argparse
import json
import csv
import sys

csv.field_size_limit(sys.maxsize)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-review_file', required=True, help='Path to review data')
        parser.add_argument('-train_file', required=True, help='Path to train file')
        parser.add_argument('-test_file', required=True, help='Path to test file')
        parser.add_argument('-business_file', required=True, help='Path to business file')
	opts = parser.parse_args()
	# f_reviews = open(opts.review_file,'r')
	f_review = open(opts.review_file,'r')
	f_train = open(opts.train_file, 'r')
	f_test = open(opts.test_file, 'r')
	f_business = open(opts.business_file, 'r')
        
        business_dic = {}
        for line in f_business:
		line = json.loads(line)
		business_dic[line['business_id']] = line

	tot = {}
	label = {}
	for line in f_train:
		l = line.split()
		tot[l[0]] = 1
		label[l[0]] = l[1]
	for line in f_test:
		l = line.split()
		tot[l[0]] = 0
		label[l[0]] = l[1]
        business = {}
	for line in f_review:
		line = json.loads(line)
		if line['business_id'] not in business:
                        business[line['business_id']] = {}
			business[line['business_id']]['label'] = label[line['business_id']]
			business[line['business_id']]['text'] = line['text'].encode('utf-8').replace('\n', '')
		else:
			business[line['business_id']]['text'] = business[line['business_id']]['text'] + ' ' + line['text'].encode('utf-8').replace('\n', '')

        for bid in business:
		if 'Wi-Fi' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNWIFI'
		elif business_dic[bid]['attributes']['Wi-Fi'] == 'paid':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_PAIDWIFI'
		elif business_dic[bid]['attributes']['Wi-Fi'] == 'free':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_FREEWIFI'
		elif business_dic[bid]['attributes']['Wi-Fi'] == 'no':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOWIFI'

		if 'Wheelchair Accessible' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNWHEELCHAIR'
		elif business_dic[bid]['attributes']['Wheelchair Accessible'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESWHEELCHAIR'
		elif business_dic[bid]['attributes']['Wheelchair Accessible'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOWHEELCHAIR'

		if 'Good for Kids' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNKIDS'
		elif business_dic[bid]['attributes']['Good for Kids'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESKIDS'
		elif business_dic[bid]['attributes']['Good for Kids'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOKIDS'

                if 'Accepts Credit Cards' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNCREDIT'
		elif business_dic[bid]['attributes']['Accepts Credit Cards'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESCREDIT'
		elif business_dic[bid]['attributes']['Accepts Credit Cards'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOCREDIT'

                if 'Good For Groups' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNGROUPS'
		elif business_dic[bid]['attributes']['Good For Groups'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESGROUPS'
		elif business_dic[bid]['attributes']['Good For Groups'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOGROUPS'

                if 'Noise Level' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNNOISE'
		elif business_dic[bid]['attributes']['Noise Level'] == 'loud':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_LOUDNOISE'
		elif business_dic[bid]['attributes']['Noise Level'] == 'average':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_AVERAGENOISE'
		elif business_dic[bid]['attributes']['Noise Level'] == 'quiet':
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_QUIETNOISE'

                if 'Outdoor Seating' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNOUTDOOR'
		elif business_dic[bid]['attributes']['Outdoor Seating'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESOUTDOOR'
		elif business_dic[bid]['attributes']['Outdoor Seating'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOOUTDOOR'
   
                if 'Delivery' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNDELIVERY'
		elif business_dic[bid]['attributes']['Delivery'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESDELIVERY'
		elif business_dic[bid]['attributes']['Delivery'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NODELIVERY'

                if 'Takes Reservations' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNRESERVATION'
		elif business_dic[bid]['attributes']['Takes Reservations'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESRESERVATION'
		elif business_dic[bid]['attributes']['Takes Reservations'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NORESERVATION'

		if 'Has TV' not in business_dic[bid]['attributes']:
			business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_UNKNOWNTV'
		elif business_dic[bid]['attributes']['Has TV'] == 1:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_YESTV'
		elif business_dic[bid]['attributes']['Has TV'] == 0:
                        business[bid]['text'] = business[bid]['text'] + ' ' + 'FEATURE_NOTV'


        train = open('train_label_text.csv', 'w')
	writer_train = csv.writer(train)
	test = open('test_label_text.csv', 'w')
	writer_test = csv.writer(test)
	for key in business:
		if tot[key] == 1:
			writer_train.writerow([key, business[key]['label'], business[key]['text']])
		elif tot[key] == 0:
			writer_test.writerow([key, business[key]['label'], business[key]['text']])
if __name__ == '__main__':
	main()
