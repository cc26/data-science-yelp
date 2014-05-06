import argparse
import json 
import re
import porter_stemmer
import threading
import thread
import time
import Queue
import sys
import urllib2
import json

q = Queue.Queue()
# retrieve a list of postings containing a 
# business id, review id, and position of each term occurrence. 
# instead of using the review id, 
# use the line on which the review occurs in the yelp dataset file as a unique identifier
stopwords = []
term_map = {}

def create_entry(line, line_number):
    text = line['text'].split()
    for i in range(0, len(text)):   
        term = term_re_process(text[i])
        if term in stopwords: 
            continue
        if term =='': 
            continue
        if term in term_map:
            term_map[term].append({"r_id":line_number,"b_id":  line['business_id'],"idx": i})
        else:
            term_map[term] = [{"r_id":line_number,"b_id":  line['business_id'],"idx": i}]


def put_queue(file_content):
    for idx in range(0,len(file_content)-1):
        q.put([json.loads(file_content[idx]),idx])

def worker(queue):
    queue_full = True
    while(queue_full):
        try:
            ele = queue.get()
            create_entry(ele[0],ele[1])
            q.task_done()

        except Queue.Empty:
        # print "Queue is empty"
            queue_full = False

def term_re_process(term):
    
    term = re.sub(r'[^\w\s]','',term)
    term = re.sub('[^\x20-\x7E]*','',term)
    term = porter_stemmer.PorterStemmer().stem(term, 0,len(term)-1).encode('utf-8')
    return term.lower()


def load_stop_words():
    stop_words_file = open('./stopwords.txt')
    for ele in stop_words_file:
        stopwords.append(ele.strip('\n'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', required=True, help='Path to input data')
    opts = parser.parse_args()

    f = open(opts.input)
    data = f.read().split('\n')
    put_queue(data)

    thread_count = 100
    thread_list = []

    for i in range(thread_count):
        t = threading.Thread(target=worker, args = (q,))
        t.daemon = True
        t.start()
        thread_list.append(t)

    q.join()
    load_stop_words()


    with open('output.json', 'w') as outfile:
        json.dump(term_map, outfile)

if __name__ == '__main__':
    main()
