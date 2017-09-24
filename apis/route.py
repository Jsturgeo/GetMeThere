class Route:
	def __init__(self, legs):
		'''
		legs: list of <Leg> objects 
		'''
		self.legs = legs

	@classmethod
	def cost(self):
		return sum(l.cost for l in self.legs)

	@classmethod
	def duration(self):
		return sum(l.duration for l in self.legs)