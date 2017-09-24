#!/usr/bin/env python
"""Returns possible routes based on user input coordinates.

Command line::

    Usage:
        routes.py <origin> <destination>
        routes.py -h | --help

    Arguments:
        origin:       Origin, string (address or lat, long: 41.43206,-81.38992)
        destination:  Destination, same format as origin

    Options:
        -h --help           Show this page.
"""
import os

from datetime import datetime

from docopt import docopt

import modo_api
import mobi_api
import google_maps_api

from leg import Leg
from route import Route

def get_routes(origin, destination):
    '''Returns possible routes based on user input coordinates.abs

    Arguments:
         origin:       Origin, string (address or lat, long: 41.43206,-81.38992)
         destination:  Destination, same format as origin

    Returns:
        {legs, summary}:
            where
            legs: list of dictionaries with keys 'start_coord', 'end_coord',
                                'mode', 'distance', 'duration', 'provider'
                                 Meters and seconds.
            summary: {'distance', 'duration'}. Meters and seconds.
    '''

    provider_names = ['mobi']
    provider_routers = [mobi_api.get_trips_routes]

    for i, provider_name in enumerate(provider_names):
        provider_name = provider_names[i]
        provider_router = provider_routers[i]
        print(provider_name)
        # route = provider_router(origin, destination)


    return 1

if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    info = get_routes(
        args['<origin>'],
        args['<destination>'])
    print(info)
