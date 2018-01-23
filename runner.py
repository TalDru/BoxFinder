#!/usr/bin/env python

import cv2
import camera
import worker
import time
import coordinates
import network

print("Launched!")

network     = network.Network()
camera      = camera.Camera()
#test        = vladivostok.NiKlass()

def run():
	picture = camera.tomat()
	#coordinates = worker.process(picture)
	#network.send(coordinates)
	#test.dudu(picture)
	cv2.imshow("dudu", worker.filterbyshape(picture))
	
while 1==1:
	run()
	time.sleep(0.02)