import argparse
import json 

# retrieve a list of postings containing a 
# business id, review id, and position of each term occurrence. 
# instead of using the review id, 
# use the line on which the review occurs in the yelp dataset file as a unique identifier

def create_index(data):


	for line in data:
		line_json = json.loads(line)

def create_entry(line):
	entry = {}

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', required=True, help='Path to data')
	opts = parser.parse_args()
	
	data = open(opts.path)
	create_index(data)

	data.close()
if __name__ == '__main__':
	main()
