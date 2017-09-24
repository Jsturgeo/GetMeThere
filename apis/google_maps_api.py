#!/usr/bin/env python
"""Returns distance and duration based on two points and mode.

Command line::

    Usage:
        google_maps_api.py <origin> <destination> [--mode <mode>]
        google_maps_api.py -h | --help

    Arguments:
        origin:       Origin, string (address or lat, long: 41.43206,-81.38992)
        destination:  Destination, same format as origin

    Options:
        -h --help           Show this page.
        --mode <mode>       One of the following: 'driving', 'walking',
                            'bicycling', 'transit'. [default: walking]
"""

import os
from datetime import datetime

from docopt import docopt
import googlemaps
from dotenv import load_dotenv, find_dotenv

MODES = ['driving', 'walking', 'bicycling', 'transit']

def fit_with_distance_duration(legs):
    '''Enriches list of legs with information on travel distance and duration.

    Arguments:
    legs:  dictionary with keys 'start_coord', 'end_coord', 'mode'

    Returns:
    dictionary with keys: 'start_coord', 'end_coord',
                          'mode', 'distance', 'duration'.
                          Meters and seconds.
    '''
    for leg in legs:
        dist_dur = get_distance_duration(leg['start_coord'], leg['end_coord'],
                                         leg['mode'])
        distance = dist_dur['distance']['value']
        duration = dist_dur['duration']['value']
        leg['distance'] = distance
        leg['duration'] = duration
    return leg

def get_distance_duration(origin, destination, mode='walking'):
    '''Returns distance and duration based on two points and mode.

    Mode should be one of 'driving', 'walking', 'bicycling', 'transit'.
    Default value is 'walking'.

    Returns:
        Dictionary {'distance': {'text': '15.7 km', 'value': 15663},
                'duration': {'text': '1 hour 8 mins', 'value': 4054},
                'status': 'OK'}
        'value' is meters for the distance and seconds for the duration.
    '''
    now = datetime.now()
    directions_result = gmaps.distance_matrix(origin,
                                              destination,
                                              mode=mode,
                                              departure_time=now)
    res = directions_result['rows'][0]['elements'][0]
    return res

load_dotenv(find_dotenv())
gmaps = googlemaps.Client(key=os.environ.get('GMAP_API_KEY'))

if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    info = get_distance_duration(
        args['<origin>'],
        args['<destination>'],
        args['--mode'])
    print(info)
