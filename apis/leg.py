class Leg:
	def __init__(self, start_coords, end_coords, mode, service, additional_data=None):
		'''
		start_coords: [<longitude>, <latitude>]
		end_coords: [<longitude>, <latitude>]
		mode: (string) one of 'walking', 'bicycling', 'driving'
		'''
		self.start_coords = start_coords
		self.end_coords = end_coords
		self.mode = mode
		self.service = service
		self.cost = None
		self.duration = None
		self.additional_data = additional_data