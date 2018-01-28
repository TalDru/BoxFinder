#!/usr/bin/env python

import cv2
import camera
import worker
import time
import coordinates
import network

#to be removed after deployment
class PictureStorage:
        picture = None
        
        def __init__(self):
                return
#end

print("Launched!")

camera   = camera.Camera()
storage     = PictureStorage()
network = network.Network()
coordinates = coordinates.Coordinates()

def click_get_hsv(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
                hsv = worker.converttohsv(storage.picture)
                print("("+str(x)+","+str(y)+"): "+str(hsv[y][x]))

def run():
	picture = camera.tomat()
	storage.picture = picture
	cv2.imshow("Original", picture)
	cv2.setMouseCallback("Original", click_get_hsv)
	coordinates = worker.process2(picture)
	if (coordinates.found()):
		network.send(coordinates)
	
while 1==1:
	run()
	time.sleep(0.02)

cv2.destroyAllWindows()
