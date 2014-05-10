import json

a = {'a':"1", 'b':'2'}
with open('output.txt', 'w') as f_out:
	for k,v in a.items():
		json.dump({k:v},f_out)
		f_out.write('\n')

			
