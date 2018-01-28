#!/usr/bin/env python

import cv2
import numpy as np
import coordinates

#SHAPE FUCKER
##################
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
_width  = 320.0
_height = 240.0
_margin = 0.0
##################

corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 )
#END SHAPE FUCKEr

#dynamic variables
lower_yellow = np.array([20,100,60])
upper_yellow = np.array([50,230,200])
#lower_yellow = np.array([30,40,0])
#upper_yellow = np.array([100,100,100])
camera_width = 320
camera_fov   = 60
cube_width   = 42 #centimeters
cube_height  = 69 #changethese

#derived variables
camera_middle = camera_width / 2
camera_single = camera_width / camera_fov
coordinates   = coordinates.Coordinates()

#functions
def process2(picture):
        blurred = blur(picture)
        cv2.imshow("blurred", blurred)
        hsv = converttohsv(blurred)
        cfilter = filterbycolor(hsv)
        cv2.imshow("mask", cfilter)
        masked = cv2.bitwise_and(blurred,blurred,mask=cfilter)
        cv2.imshow("masked", masked)
        smallest, biggest, cX, cY, area = filterbyshape(masked)
        coordinates = getcoords2(smallest, biggest, cX, cY, area)
        cv2.waitKey(27) & 0xFF == ord('q')
        return coordinates

def process(picture): #TODO revise processing model
	blurred = blur(picture)
	hsv = converttohsv(blurred)
	cfilter = filterbycolor(hsv)
	cv2.waitKey(27) & 0xFF == ord('q')
	return hsv
	#sfilter = filterbyshape(cfilter)
	#keypoints = getkeypoints(sfilter)
	#coordinates = getcoords(keypoints)
	#return coordinates

def blur(matrice):
	return cv2.blur(matrice,(10,10))

def converttohsv(matrice):
	return cv2.cvtColor(matrice, cv2.COLOR_BGR2HSV)

def filterbycolor(matrice):
	return cv2.inRange(matrice, lower_yellow, upper_yellow)

def filterbyshape(matrice):

	IS_FOUND = 0
	extLeft, extRight, cX, cY, area = -1, -1, -1, -1, -1

	rgb = matrice
	gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )
	gray = cv2.bilateralFilter( gray, 1, 10, 120 )
	edges  = cv2.Canny( matrice, 10, CANNY )
	kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )
	closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )
	h, contours, _ = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
	maxS = -1

	for cont in contours:
		if cv2.contourArea ( cont ) > 4250 :
			arc_len = cv2.arcLength( cont, True )
			approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )
			if ( len( approx ) >= 4 and len( approx ) <= 6 ):
				IS_FOUND = 1
				area = cv2.contourArea ( cont )
				if (area > maxS):
                                        M = cv2.moments( cont )
                                        cX = int(M["m10"] / M["m00"])
                                        cY = int(M["m01"] / M["m00"])
                                        #cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                                        pts_src = np.array( approx, np.float32 )
                                        
                                        c = cont
                                        extLeft = tuple(c[c[:, :, 0].argmin()][0])
                                        extRight = tuple(c[c[:, :, 0].argmax()][0])
                                        #extTop = tuple(c[c[:, :, 1].argmin()][0])
                                        #extBot = tuple(c[c[:, :, 1].argmax()][0])

                                        #h1, status = cv2.findHomography( pts_src, pts_dst )
                                        #out = cv2.warpPerspective( rgb, h1, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) )
                                        #cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )
			else : pass

	#if IS_FOUND :
	#	cv2.imshow('Found', out )

	return extLeft, extRight, cX, cY, area

def getkeypoints(matrice):
	#TODO
	return

def measureangle(keypoint):
	return (camera_middle - keypoint.pt.x) / camera_single

def measureangle2(cX):
	if (cX == -1):
                return -1
	return (camera_middle - cX) / camera_single

def measurealpha(cX):
	if (cX == -1):
		return -1
	return (camera_middle - cX) / camera_single

def measurebetta(smallest, biggest):
	if (smallest == -1 or biggest == -1):
		return -1
	return (biggest - smallest) / camera_single

def measuredistance(keypoint):
        #TODO
	return -1

def measuredistance2(smallest, biggest, cX):
        if (smallest == -1 or biggest == -1 or cX == -1):
                return -1
        if (smallest > biggest):
                tmp = smallest
                smallest = biggest
                biggest = tmp

        alpha = measurealpha(cX)
        betta = measurebetta(smallest, biggest)
        distance_x_1 = (cube_width * betta) / math.sin(math.radians(90 - alpha - betta))
        distance_x_2 = (cube_width * betta) / math.sin(math.radians(90 + alpha))
        distance_x = (distance_x_1 + distance_x_2) / 2
        return distance_x

def getcoords(keypoints):
	#coordinates = Coordinates()
	if (keypoints.size() != 1):
		coordinates.angle    = -1
		coordinates.distance = -1
		return coords
	coordinates.angle    = measureangle(keypoints[0])
	coordinates.distance = measuredistance(keypoints[0])
	return coords

def getcoords2(smallest, biggest, cX, cY, area):
        coordinates.angle = measureangle2(cX)
        #coordinates.distance = measuredistance2(smallest, biggest, area)
        coordinates.distance = -1
        return coordinates
