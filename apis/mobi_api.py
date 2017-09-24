import requests
import json
from haversine import haversine
from itertools import product
from google_maps_api import fit_with_distance_duration, get_directions_for_leg
from leg import Leg
from route import Route
from math import ceil

import pprint
pp = pprint.PrettyPrinter(indent=2)

mobi_url = 'https://mountainmath.ca/mobi/stations'

start_coords = [ 49.283481, -123.114867] # BCIT Downtown
end_coords =  [49.274196, -123.15113] # Kits Beach

def get_mobi_stations_data():
	response = requests.get(mobi_url)
	resp_parsed = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
	return resp_parsed['features']

def get_closest_stations(start_coords, stations_data, top_n=3):
	bikes_data = []
	for station in stations_data:
		if station['properties']['avl_bikes'] == 0 or not station['properties']['operative']:
			continue
		wrong_coordinates = station['geometry']['coordinates']
		coordinates = [wrong_coordinates[1], wrong_coordinates[0]]
		dist_from_current = haversine(coordinates, start_coords)
		bikes_data.append((dist_from_current, station['properties']['name'], coordinates))
	sorted_bikes = sorted(bikes_data, key=lambda x: x[0])
	return sorted_bikes[:top_n]

def potential_routes(start_coords, closest_stations_start, closest_stations_end, end_coords, service='mobi', method='bicycling'):
	first_legs = [Leg(start_coords, station[2], 'walking', 'None') for station in closest_stations_start]
	last_legs = [Leg(station[2], end_coords, 'walking', 'None') for station in closest_stations_end]
	first_and_last = list(product(first_legs, last_legs))
	full_routes = [(fl[0], Leg(fl[0].end_coords, fl[1].start_coords, method, service), fl[1]) for fl in first_and_last]
	return [Route(r) for r in full_routes]

def get_trips_routes(start_coords, end_coords):
	stations_data = get_mobi_stations_data()
	closest_stations_start = get_closest_stations(start_coords, stations_data)
	closest_stations_end = get_closest_stations(end_coords, stations_data)
	routes = potential_routes(start_coords, closest_stations_start, closest_stations_end, end_coords)
	return routes

def apply_route_cost(route, membership_type):
	fit_with_distance_duration(route)
	for leg in route.legs:
		if leg.mode == 'walking':
			leg.cost = 0
			continue
		total_biking_time = float(leg.duration) / 60
		if total_biking_time <= 30:
			leg.cost = 0
		overage_time = total_biking_time - 30
		if membership_type == '24_hour_pass':
			leg.cost = ceil(float(overage_time) / 30) * 5
		elif membership_type in ('90_day_pass', '365_day_pass_standard'):
			overage_cost = 2
			if overage_time > 30:
				overage_time += -30
				overage_cost += ceil(float(overage_time) / 30) * 3
			leg.cost = overage_cost
		elif membership_type == '365_day_pass_plus':
			if overage_time <= 30:
				leg.cost = 0
			overage_time += -30
			leg.cost = ceil(float(overage_time) / 30) * 3
		else: #unknown membership type
			leg.cost = 0

def get_mobi_routes(start_coords, end_coords):
	routes = get_trips_routes(start_coords, end_coords)
	for route in routes:
		#apply_route_cost(route, '24_hour_pass')
		for leg in route.legs:
			pp.pprint(get_directions_for_leg(leg))
	return routes

get_mobi_routes(start_coords, end_coords)
