import requests
import json
import time
from haversine import haversine
from google_maps_api import fit_with_distance_duration
from route import Route
from leg import Leg

start_coords = [49.283481, -123.114867] # BCIT Downtown
end_coords =  [49.274196, -123.15113] # Kits Beach

availability_url = 'https://bookit.modo.coop/api/availability/'
cost_url = 'https://bookit.modo.coop/api/cost/'

def parse_mobi_data(raw_data, start_time):
	mobi_cars = []
	for key in raw_data.keys():
		car = raw_data[key]
		if car['Duration'] == 'throttled': #or car['StartTime'] != start_time:
			continue
		mobi_cars.append(([float(car['Latitude']), float(car['Longitude'])], 
			{'description' : car['CarDescription'], 'location_name' : car['LocationName'], 'start_time' : car['StartTime'], 'end_time' : car['EndTime']}))
	return mobi_cars

def get_closest_cars(current_location, mobi_data, top_n=3):
	cars_data = []
	for car in mobi_data:
		dist_from_current = haversine(car[0], current_location)
		cars_data.append((dist_from_current, car))
	sorted_cars = sorted(cars_data, key=lambda x: x[0])
	return sorted_cars[:top_n]

def potential_routes(start_coords, closest_cars, end_coords, method='driving', service='modo'):
	first_legs = [Leg(start_coords, car[1][0], 'walking', None) for car in closest_cars]
	last_legs = [Leg(car[1][0], end_coords, method, service, additional_data=car[1][1]) for car in closest_cars]
	full_routes = zip(first_legs, last_legs)
	return [Route(r) for r in full_routes]

def get_mobi_data():
	now = int(time.time())
	response = requests.get(availability_url + str(now))
	resp_json = json.loads(response.text)
	raw_data = resp_json['Data']
	start_time = resp_json['Request']['RequestStart']
	return raw_data, start_time

def get_trips_routes(start_coords, end_coords):
	raw_data, start_time = get_mobi_data()
	parsed_data = parse_mobi_data(raw_data, start_time)
	closest_cars = get_closest_cars(start_coords, parsed_data)
	routes = potential_routes(start_coords, closest_cars, end_coords)
	return routes

def squash_coords(coords):
	return "{},{}".format(coords[0], coords[1])

def get_route_cost(route, membership_type):
	'''
	only supporting 'Roaming' and 'Business' memberships for now since I can't figure out
	why this API hates spaces in the URL
	'''
	fit_with_distance_duration(route)
	driving_distance = sum(l.distance for l in route.legs if l.mode == 'driving')
	driving_route = [l for l in route.legs if l.mode == 'driving'][0]
	url = cost_url + membership_type + '/' + driving_route.additional_data['start_time'] + '/' + driving_route.additional_data['end_time'] + '/' + str(driving_route.distance)
	response = requests.get(url)
	resp_parsed = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
	return float(resp_parsed['TotalCharge'])

# routes = get_trips_routes(start_coords, end_coords)
# for route in routes:
# 	print get_route_cost(route, 'Business')
