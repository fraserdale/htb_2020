from math import sin, cos, sqrt, atan2, radians
import requests
import numpy as np
import json
from flask import Flask, render_template, request, redirect
from math import sin, cos, sqrt, atan2, radians

# setup flask app
app = Flask(__name__)

bankInfo = []
bankLinks = [
		'https://openapi.bankofireland.com/open-banking/v2.2/atms',
		'https://api.bankofscotland.co.uk/open-banking/v2.2/atms',
		'https://atlas.api.barclays/open-banking/v2.2/atms',
		'https://obp-data.danskebank.com/open-banking/v2.2/atms',
		'https://openapi.firsttrustbank.co.uk/open-banking/v2.2/atms',
		'https://api.halifax.co.uk/open-banking/v2.2/atms',
		'https://api.hsbc.com/open-banking/v2.2/atms',
		'https://api.lloydsbank.com/open-banking/v2.2/atms',
		'https://openapi.nationwide.co.uk/open-banking/v2.2/atms',
		#
		'https://openapi.rbs.co.uk/open-banking/v2.2/atms',
		'https://openapi.natwest.com/open-banking/v2.2/atms',
		'https://openapi.ulsterbank.co.uk/open-banking/v2.2/atms'
		'https://openbanking.santander.co.uk/sanuk/external/open-banking/v2.2/atms',
	]

	#bankLinks = ['https://openapi.rbs.co.uk/open-banking/v2.2/atms']

for link in bankLinks:
	try:
		bankInfo.append(requests.get(link).json())
	except:
		continue


@app.route("/", methods=['POST'])
def home():

	print(request.json)

	lat = request.json['lat']
	lng = request.json['long']
	

	coords = []
	allatms = []
	for bank in bankInfo:
		try:
			for atm in bank['data'][0]['Brand'][0]['ATM']:
				if ([float(atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Latitude']), float(
				    atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Longitude'])]) in coords: continue
				coords.append([float(atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Latitude']), float(
				    atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Longitude'])])
				allatms.append(atm)
		except:
			continue
	# coords.sort(key=lambda x: x['Latitude'], reverse=False)

	node = [lat, lng]

	def closest_node(node, nodes):
		dist_2 = []
		for idx, n in enumerate(nodes):
			# approximate radius of earth in km
			R = 6373.0

			lat1 = radians(node[0])
			lon1 = radians(node[1])
			lat2 = radians(n[0])
			lon2 = radians(n[1])

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = R * c

			dist_2.append((distance,idx))

			# dist_2.append((((node[0] - n[0]) + (node[1] - n[1]))**2, idx))

		dist_2.sort(key=lambda x: x[0])

		print(dist_2[:10])

		return dist_2[:10]
		# nodes = np.asarray(nodes)
		# dist_2 = np.sum((nodes - node)**2, axis=1)
		# print(np.argmin(dist_2))
		# return np.argmin(dist_2)

	nearest10 = []
	for x in closest_node(node,coords):
		nearest10.append(allatms[x[1]])

	print(nearest10)
	return (json.dumps({"data":nearest10}))

if __name__ == "__main__":
	app.run(port=3000,debug=False)
