from collections import deque

class MovingAverageFilter:
	def __init__(self, windowSize):
		self.sum = 0
		self.count = 0
		self.windowSize = windowSize
		self.average = 0
		self.leastRecent = 0
		self.name = "movingAverage"
		self.q = deque()

	def filter(self, measurement):
		if self.count < self.windowSize :
			self.count += 1
		else :
			self.leastRecent = self.q.popleft()

		self.q.append(measurement)
		self.sum -= self.leastRecent
		self.sum += measurement
		self.average = self.sum/self.count
		return self.average

	def get_name(self):
		return self.name