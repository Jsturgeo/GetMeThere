
# coding: utf-8

get_ipython().system(u'pip install uber-rides')
get_ipython().system(u'pip install python-dotenv')

import json
import os
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
server_token=os.environ.get('UBER_SERVER_TOKEN')

start_coords = [-122.418075, 37.7752315]
end_coords =  [-122.405, 37.791]


def get_uber_data(start_coords, end_coords):
    session = Session(server_token)
    client = UberRidesClient(session)
    time = client.get_pickup_time_estimates(start_latitude=start_coords[1], start_longitude=start_coords[0])
    price = client.get_price_estimates(start_latitude=start_coords[1], start_longitude=start_coords[0], 
                                       end_latitude=end_coords[1], end_longitude=end_coords[0],seat_count=1)
    time_estimate= time.json.get('times')
    price_estimate = price.json.get('prices')
    result = [{start_coord: start_coords, end_coord: start_coords, mode: 'waiting', duration: 0, cost: 0},
              {start_coord: start_coords, end_coord: end_coords, mode: 'taxi', duration: 0, cost: 0}]
    #result (start_coords, end_coords, mode, distance, duration, cost) return routes 1list : 2 dict for each leg ()
    
    return price_estimate, time_estimate


price_estimate, time_estimate = get_uber_data(start_coords, end_coords)

print json.dumps(price_estimate, indent=4, sort_keys=True)


print json.dumps(time_estimate, indent=4, sort_keys=True)




