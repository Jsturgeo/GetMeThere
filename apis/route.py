class Route:
	def __init__(self, legs):
		'''
		legs: list of <Leg> objects 
		'''
		self.legs = legs

	@property
	def cost(self):
		costs = [0 if x.cost is None else x.cost for x in self.legs]
		return sum(costs)

	@property
	def duration(self):
		durations = [0 if x.duration is None else x.duration for x in self.legs]
		return sum(durations)
		# return sum(l.duration for l in self.legs)

	@property
	def total_walk_time(self):
		walking_legs = [x for x in self.legs if x.mode == 'walking']
		durations = [0 if x.duration is None else x.duration for x in walking_legs]
		return sum(durations)

	def __str__(self):
		return str('Duration: {} minutes, Cost: {}, Legs: {}'.format(int(float(self.duration) / 60), self.cost, [(l.start_coords, l.end_coords, l.mode) for l in self.legs]))
