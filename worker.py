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
_width  = 480.0
_height = 320.0
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
lower_yellow = np.array([52,69,40])
upper_yellow = np.array([70,90,80])
#lower_yellow = np.array([30,40,0])
#upper_yellow = np.array([100,100,100])
camera_width = 480
camera_fov   = 60

#derived variables
camera_middle = camera_width / 2
camera_single = camera_width / camera_fov

#functions
def process(picture): #TODO revise processing model
	blurred = blur(picture)
	hsv = converttohsv(blurred)
	cfilter = filterbycolor(hsv)
	return hsv
	#sfilter = filterbyshape(cfilter)
	#keypoints = getkeypoints(sfilter)
	#coordinates = getcoords(keypoints)
	#return coordinates

def blur(matrice):
	return cv2.blur(matrice,(5,5))

def converttohsv(matrice):
	return cv2.cvtColor(matrice, cv2.COLOR_BGR2HSV)

def filterbycolor(matrice):
	return cv2.inRange(matrice, lower_yellow, upper_yellow)

def filterbyshape(matrice):
	rgb = matrice
	gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )
	gray = cv2.bilateralFilter( gray, 1, 10, 120 )
	edges  = cv2.Canny( gray, 10, CANNY )
	kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )
	closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )
	contours, h, _ = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

	for cont in h:
		if cv2.contourArea ( cont ) > 5000 :
			arc_len = cv2.arcLength( cont, True )
			approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )
			if ( len( approx ) == 4 ):
				IS_FOUND = 1
				#M = cv2.moments( cont )
				#cX = int(M["m10"] / M["m00"])
				#cY = int(M["m01"] / M["m00"])
				#cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
				pts_src = np.array( approx, np.float32 )

				h, status = cv2.findHomography( pts_src, pts_dst )
				out = cv2.warpPerspective( rgb, h, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) )
				cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )
			else : pass

	#current = str(time.time())
    #cv2.namedWindow( 'edges', cv2.CV_WINDOW_AUTOSIZE )
	#cv2.imshow( 'edges', edges )
	#cv2.imwrite("edges_"+current+".jpg", edges)
	#cv2.namedWindow( 'rgb', cv2.CV_WINDOW_AUTOSIZE )
	#cv2.imshow( 'rgb', rgb )
	#cv2.imwrite("rgb_"+current+".jpg", rgb)
	
	#if IS_FOUND :
	#	#cv2.namedWindow( 'out', cv2.CV_WINDOW_AUTOSIZE )
	#	#cv2.imshow( 'out', out )
	#	#cv2.imwrite("out_"+current+".jpg", out)
	#	IS_FOUND = 0
	cv2.waitKey(27) & 0xFF == ord('q')
	return edges

def getkeypoints(matrice):
	#TODO
	return

def getcoords(keypoints):
	coordinates = Coordinates()
	if (keypoints.size() != 1):
		coordinates.angle    = -1
		coordinates.distance = -1
		return coords
	coordinates.angle    = measureangle(keypoints[0])
	coordinates.distance = measuredistance(keypoints[0])
	return coords

def measureangle(keypoint):
	return (camera_middle - keypoint.pt.x) / camera_single

def measuredistance(keypoint):
	#TODO
	return
