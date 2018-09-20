class SerialInstr:
	def __init__(self, comport, baudrate, stopbit, polarity):
		self.port = 'ASRL'
		self.port += comport
		self.port += '::INSTR'
		self.rm = visa.ResourceManager
		self.instrment = self.rm.open_resource(self.port)
	def Open(self):
		self.rm = visa.ResourceManager
		self.instrment = rm.open_resource(self.port)