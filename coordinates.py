#!/usr/bin/env python

class Coordinates:

	def __init__(self):
		self.angle    = -1
		self.distance = -1

	def __str__(self):
		return str(self.angle)+","+str(self.distance)

	def found(self):
                if (self.angle == -1):
                        return False
                return True
