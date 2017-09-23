import requests
import json
import pprint
import time
from haversine import haversine

current_location = [-123.114867, 49.283481]
destination_coords =  [-123.15113, 49.274196]#[-123.092092, 49.262653]

pp = pprint.PrettyPrinter(indent=4)

locations_url = 'https://bookit.modo.coop/api/fleet/locations'
neighborhoods_url = 'https://bookit.modo.coop/api/fleet/neighbourhoods'
availability_url = 'https://bookit.modo.coop/api/availability'




def parse_mobi_data(raw_data):
	mobi_cars = []
	for key in raw_data.keys():
		car = raw_data[key]
		if car['Duration'] == 'throttled':
			continue
		mobi_cars.append((car['CarID'], [float(car['Longitude']), float(car['Latitude'])], car['Duration'], car['CarDescription'], car['LocationName']))
	return mobi_cars

def get_closest_cars(current_location, mobi_data, top_n=3):
	cars_data = []
	for car in mobi_data:
		dist_from_current = haversine(car[1], current_location)
		cars_data.append((dist_from_current, car))
	sorted_cars = sorted(cars_data, key=lambda x: x[0])
	return sorted_cars[:top_n]

def potential_routes(current_location, closest_cars, destination_coords, method='drive'):
	first_legs = [{'start_coord' : current_location, 'end_coord' : car[1][1], 'mode' : 'walk'} for car in closest_cars]
	last_legs = [{'start_coord' : car[1][1], 'end_coord' : destination_coords, 'mode' : method} for car in closest_cars]
	full_routes = zip(first_legs, last_legs)
	return full_routes

def get_mobi_data():
	now = int(time.time())
	response = requests.get(availability_url + '/' + str(now))
	resp_json = json.loads(response.text)
	raw_data = resp_json['Data']
	return raw_data


def get_trips_routes():
	raw_data = get_mobi_data()
	parsed_data = parse_mobi_data(raw_data)
	closest_cars = get_closest_cars(current_location, parsed_data)
	routes = potential_routes(current_location, closest_cars, destination_coords, method='drive')
	return routes