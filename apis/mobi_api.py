import requests
import json
from haversine import haversine
from itertools import product


mobi_url = 'https://mountainmath.ca/mobi/stations'

current_location = [-123.114867, 49.283481]
destination_coords =  [-123.092092, 49.262653]

def get_mobi_stations_data():
	response = requests.get(mobi_url)
	resp_parsed = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
	return resp_parsed['features']

def get_closest_stations(current_location, stations_data, top_n=3):
	bikes_data = []
	for station in stations_data:
		if station['properties']['avl_bikes'] == 0 or not station['properties']['operative']:
			continue
		dist_from_current = haversine(station['geometry']['coordinates'], current_location)
		bikes_data.append((dist_from_current, station['properties']['name'], station['geometry']['coordinates']))
	sorted_bikes = sorted(bikes_data, key=lambda x: x[0])
	return sorted_bikes[:top_n]

def potential_legs(current_location, closest_stations_start, closest_stations_end, destination_coords, method='bike'):
	first_legs = [(current_location, station[2], 'walk') for station in closest_stations_start]
	last_legs = [(station[2], destination_coords, 'walk') for station in closest_stations_end]
	first_and_last = product(first_legs, last_legs)
	full_legs = [(fl[0], (fl[0][1], fl[1][0], method), fl[1]) for fl in first_and_last]
	return full_legs

def get_trips_legs():
	stations_data = get_mobi_stations_data()
	closest_stations_start = get_closest_stations(current_location, stations_data)
	closest_stations_end = get_closest_stations(destination_coords, stations_data)
	legs = potential_legs(current_location, closest_stations_start, closest_stations_end, destination_coords)
	return legs


