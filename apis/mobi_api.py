import requests
import json
from haversine import haversine
from itertools import product

mobi_url = 'https://mountainmath.ca/mobi/stations'

start_coords = [-123.114867, 49.283481] # BCIT Downtown
end_coords =  [-123.15113, 49.274196] # Kits Beach

def get_mobi_stations_data():
	response = requests.get(mobi_url)
	resp_parsed = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
	return resp_parsed['features']

def get_closest_stations(start_coords, stations_data, top_n=3):
	bikes_data = []
	for station in stations_data:
		if station['properties']['avl_bikes'] == 0 or not station['properties']['operative']:
			continue
		dist_from_current = haversine(station['geometry']['coordinates'], current_coords)
		bikes_data.append((dist_from_current, station['properties']['name'], station['geometry']['coordinates']))
	sorted_bikes = sorted(bikes_data, key=lambda x: x[0])
	return sorted_bikes[:top_n]

def potential_routes(start_coords, closest_stations_start, closest_stations_end, end_coords, method='bicycling'):
	first_legs = [{'start_coords' : current_coords, 'end_coords' : station[2], 'mode' : 'walking'} for station in closest_stations_start]
	last_legs = [{'start_coords' : station[2], 'end_coords' : end_coords, 'mode' : 'walking'} for station in closest_stations_end]
	first_and_last = list(product(first_legs, last_legs))
	full_routes = [(fl[0], {'start_coords' : fl[0]['end_coords'], 'end_coords' : fl[1]['start_coords'], 'mode' : method}, fl[1]) for fl in first_and_last]
	return full_routes

def get_trips_routes(start_coords, end_coords):
	stations_data = get_mobi_stations_data()
	closest_stations_start = get_closest_stations(start_coords, stations_data)
	closest_stations_end = get_closest_stations(end_coords, stations_data)
	routes = potential_routes(start_coords, closest_stations_start, closest_stations_end, end_coords)
	return routes

def get_route_cost(route, membership_type):
	total_biking_time = sum(l['duration'] for l in route if l['mode'] == 'biking')
	if total_biking_time <= 30:
		return 0
	overage_time = total_biking_time - 30
	if membership_type == '24_hour_pass':
		return ceil(float(overage_time) / 30) * 5
	elif membership_type in ('90_day_pass', '365_day_pass_standard'):
		overage_cost = 2
		if overage_time > 30:
			overage_time += -30
			overage_cost += ceil(float(overage_time) / 30) * 3
		return overage_cost
	elif membership_type == '365_day_pass_plus':
		if overage_time <= 30:
			return 0
		overage_time += -30
		return ceil(float(overage_time) / 30) * 3
	else: #unknown membership type
		return 0