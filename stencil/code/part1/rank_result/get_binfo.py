#!/usr/bin/python
import sys
import json
from csv import writer
business_file = "/course/cs1951a/pub/final/data/extracted/yelp_academic_dataset_business.json"
rank_res = "rank_result"

f_rank = open(rank_res, 'r')
f_o = open('q.csv','w')
cw = writer(f_o)

b_map = {}
f_b = open(business_file,'r')
line_num = 0
for line in f_b:
	b_json = json.loads(line)
	b_map[b_json['business_id']]=b_json
	line_num += 1

# list_in = sys.argv[1]
# list_in = "[u'6DaBdOr7NNsIWBC_2zty7A', u'hx9dmPZZHvLQgEhlAZ-Seg', u'i4X_iu_29PkhL2zsIRpueQ', u'wxQamxLLHo_2d5Kgs70kOw', u'2OHzwWxfl3DsHdAcRZOykA', u'jMIuId3VIGhsateF-Wg2zA', u'wnkCMnBVkQM5td24gHkLpA', u'5G_oPzPhlTJ1zMmqywWOUw', u'xEwujSrjqGK_dWJ28YSQiQ', u'Ct2ioh5hZ83X2ycLSQoKbA']"

# for line in fileinput.input():
#     s = line.decode('utf8')
#     print s.translate(table),

def processLine(list_in):
	list_in = list_in.strip()
	print list_in
	bids = list_in.strip("[").strip("]").split(", ")
	bids = [b[2:-1] for b in bids]

	for bid in bids:
		row = []
		row.append(b_map[bid]['name'].encode('utf8'))
		row.append(b_map[bid]['business_id'])
		row.append(b_map[bid]['full_address'].replace('\n',','))
		row.append(str(b_map[bid]['stars']))
		row.append(str(b_map[bid]['review_count']))
		cate_str = ""
		for c in b_map[bid]['categories']:
			cate_str+=c+","
		cate_str.strip(",")
		row.append(cate_str[:-1])
		
		cw.writerow(row)

for line in f_rank:
	if line.startswith('['):
		processLine(line)
	else:
		cw.writerow([line])
