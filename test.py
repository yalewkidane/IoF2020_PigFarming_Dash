import requests
import argparse
import time
import random
import json


def post(url, payload):


	# POST with form-encoded data
	#r = requests.post(url, data=payload)

	# POST with JSON 
	#import json

	headers = {'Content-Type':'application/json'}

	r = requests.post(url, headers=headers, data=json.dumps(payload))


	# Response, status etc
	print(r.text)
	print(r.status_code)

def get(url):

	# GET with params in URL
	#r = requests.get(url, params=payload)

	# GET
	r = requests.get(url)
	# Response, status etc
	r.text
	r.status_code


Pyload = {
	"F_consumption":
	{
	    "date":["4", "5", "6"], 
	    "value":["6", "7", "7"] 
	}, 
	
	"W_consumption":{
	    "date":["1", "2", "3"], 
	    "value":["1", "2", "3"]
	},
	"weight":{
	    "date":["1", "2", "3"], 
	    "value":["10", "20", "30"]
	}, 
	
	"growth":{
	    "date":["1", "2", "3"], 
	    "value":["11", "21", "31"]
	}
    
}

def make_payload(i):
	new_payload = Pyload
	new_payload['F_consumption']['date']= [i]
	new_payload['F_consumption']['value']= [random.randint(1,51)]

	new_payload['W_consumption']['date']= [i]
	new_payload['W_consumption']['value']= [random.randint(1,51)]

	new_payload['weight']['date']= [i]
	new_payload['weight']['value']= [random.randint(1,51)]

	new_payload['growth']['date']= [i]
	new_payload['growth']['value']= [random.randint(1,51)]

	return new_payload



if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='IoF2020 Pig Farming Dashboard')
	parser.add_argument('--host', type=str, default= '127.0.0.1', 
	    help='The host ip address where the dashboard runs' )
	parser.add_argument('--port', type=int, default= 8080, 
	    help='The host port address where the dashboard runs' )

	args = parser.parse_args()

	pig_ids = ['pig_1', 'pig_2']

	i=0
	while 1:
		print('loop' + str(i))
		for pig_id in pig_ids:
			post('http://'+args.host+':'+str(args.port)+'/pig/'+ str(pig_id), make_payload(i))

		i +=1
		time.sleep(5)




