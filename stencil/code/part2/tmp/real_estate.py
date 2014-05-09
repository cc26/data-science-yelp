import urllib
import urllib2
import xml.etree.ElementTree as ET
import csv
import sys
import json
result = []
def get_price_range(address, citystatezip, business, full_addr):
	# 1111+E+Buckeye+Rd
	# a = "1111 E Buckeye Rd\nPhoenix, AZ 85034"
	# x = '2114 Bigelow Ave'
	# y = 'Seattle, WA'
	# address = '1501 W Bell Rd'
	# citystatezip = 'Phoenix, AZ 85023'
	params = urllib.urlencode({'zws-id': 'X1-ZWz1dt8307680b_634pb', 'address': address, 'citystatezip': citystatezip, 'rentzestimate':'true'})
	# print params
	# params = "zws-id=X1-ZWz1dt8307680b_634pb&citystatezip=Glendale%2C+AZ+85301&rentzestimate=true&address=5630+W+Camelback+Rd"
	# print params
	r = urllib2.urlopen("http://www.zillow.com/webservice/GetSearchResults.htm?%s", params).read()
	# print r
	root = ET.fromstring(r)

	item = root.iter('valuationRange')
	
	price_list = []
	for line in item:
	 	price_list.append( (line[0].text, line[1].text))
	# print price_list
	if not price_list:
		return
	else:
		result.append({'business':business, 'address':full_addr, 'prices':price_list})

def get_rent_list(f):
	data = csv.reader(f)
	
	for line in data:
		buss = line[0]
		full_addr = line[1].split('\n')
		addr = full_addr[0]
		citystatezip = full_addr[1]
		get_price_range(addr, citystatezip, buss, full_addr)
		# break
	with open(sys.argv[2], 'w') as f_out:
		json.dump(result, f_out)




if __name__ == '__main__':
	get_rent_list(open(sys.argv[1]))