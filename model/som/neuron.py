#Class to represents the neurons in a gsom.
#Each neuron has a reference(a list) to its surrounding neighbours.
#The maximum number of neighbours a neuron can hold is 4.
#Because a rectangular cluster is assumed.
#Each neuron also holds a weight vector.
#x and y positions  are used to map the position of the neuron on the grid.
class neuron:
	def __init__(self,weightVector,accumulatedError):
		
		self.weightVector = weightVector
		self.accumulatedError = accumulatedError
		
		
		
	#Returns the list of neighbours of the neuron.
	#def getNeighbours(self):
	#	return self.neighbours
		
	#Sets the list of neighbours of a neuron.	
	#def setNeighbours(self,neighbours):
	#	self.neighbours = neighbours
		
	#Append a  new neighbour	
	#def addNeighbour(self,neighbourNeuron):
	#	self.neighbours.append(neighbourNeuron)
		
	#Sets the weight vector
	def setweightVector(self,weightVector):
		self.weightVector = weightVector
	#Get the weight vector
	def getweightVector(self):
		return self.weightVector
	#Set the total error value	
	def setAccumulatedError(self,error):
		 self.accumulatedError = error
	#Get accumulatedError
	def getAccumulatedError(self):
		return self.accumulatedError
