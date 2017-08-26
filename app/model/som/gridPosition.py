#classs to represent the grid position of the neurons.#Objects of this class is to be used as keys
#for the neurons to represent their positions in the grid.
class gridPosition:
    
	def __init__(self, xPosition, yPosition):
		self.xPosition = xPosition
		self.yPosition = yPosition

	def getXposition(self):
		return self.xPosition

	def setYposition(self, yPosition):
		self.yPosition = yPosition

	def getYposition(self):
		return self.yPosition

	def __hash__(self):
		return hash((self.xPosition, self.yPosition))

	def __eq__(self, other):
		return (self.xPosition, self.yPosition) == (other.xPosition, other.yPosition)

	def setXposition(self, xPosition):
		self.xPosition = xPosition
