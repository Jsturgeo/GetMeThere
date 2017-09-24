class Route:
	def __init__(self, legs):
		'''
		legs: list of <Leg> objects 
		'''
		self.legs = legs

	@property
	def cost(self):
		return sum(l.cost for l in self.legs)

	@property
	def duration(self):
		return sum(l.duration for l in self.legs)

	@property
	def total_walk_time(self):
		return sum(l.duration for l in self.legs if l.mode == 'walking')

	def __str__(self):
		return str('Duration: {} minutes, Cost: {}, Legs: {}'.format(int(float(self.duration) / 60), self.cost, [(l.start_coords, l.end_coords, l.mode) for l in self.legs]))
