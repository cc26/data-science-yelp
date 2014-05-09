import csv
import sys
import json

def getlist(f):
	data = json.load(f)
	count = 1
	for line in data:
		for ele in line['prices']:
			low = ele[0]
			high = ele[1]
			if low != None and high != None and int(high) < 10000:
				print str(count)+'\t'+low+'\t'+high
				count += 1

if __name__ == '__main__':
	getlist(open(sys.argv[1]))