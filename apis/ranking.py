from mobi_api import get_mobi_routes
from modo_api import get_modo_routes

start_coords = [ 49.283481, -123.114867] # BCIT Downtown
end_coords =  [49.274196, -123.15113] # Kits Beach

all_routes = get_modo_routes(start_coords, end_coords) + get_mobi_routes(start_coords, end_coords)

def cheapest_trip(routes):
	return sorted(routes, key=lambda r: (r.cost, r.duration))[0]

def shortest_time(routes):
	return sorted(routes, key=lambda r: (r.duration, r.cost))[0]

print cheapest_trip(all_routes)
print shortest_time(all_routes)