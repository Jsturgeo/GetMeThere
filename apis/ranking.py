from mobi_api import get_mobi_routes
from modo_api import get_modo_routes

start_coords = [ 49.283481, -123.114867] # BCIT Downtown
end_coords =  [49.274196, -123.15113] # Kits Beach

all_routes = get_modo_routes(start_coords, end_coords) + get_mobi_routes(start_coords, end_coords)

def cheapest_trip(routes):
	return sorted(routes, key=lambda r: (r.cost, r.duration))

def shortest_time(routes):
	# return sorted(routes, key=lambda r: (r.duration['value'], r.cost))[0]
	# return sorted(routes, key=lambda r: (r.duration))
	return sorted(routes, key=lambda r: (r.duration if not (r.duration is None) else 1e9))

print "Cheapest one:"
print cheapest_trip(all_routes)[0]
print "Shortest one:"
print shortest_time(all_routes)[0]