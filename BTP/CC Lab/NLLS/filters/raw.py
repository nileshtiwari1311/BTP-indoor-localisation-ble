class RawFilter:
	def __init__(self):
		self.name = "raw"

	def filter(self, measurement) :
		return measurement

	def get_name(self) :
		return self.name