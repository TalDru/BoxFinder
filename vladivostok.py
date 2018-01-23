#!/usr/bin/env python

#-*- coding: utf-8 -*-

import cv2
import time
import numpy as np


class NiKlass: 
	
	def __init__(self):
		##################
		self.IS_FOUND = 0

		self.MORPH = 7
		self.CANNY = 250
		##################
		self._width  = 480.0
		self._height = 320.0
		self._margin = 0.0
		##################

		self.corners = np.array(
			[
				[[  		self._margin, self._margin 			]],
				[[ 			self._margin, self._height + self._margin  ]],
				[[ self._width + self._margin, self._height + self._margin  ]],
				[[ self._width + self._margin, self._margin 			]],
			]
		)
		
		self.pts_dst = np.array( self.corners, np.float32 )
	
		
	def filterbyshape(self,matrice):
		rgb = matrice
		gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
		gray = cv2.bilateralFilter(gray, 1, 10, 120)
		edges  = cv2.Canny( gray, 10, self.CANNY )
		kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( self.MORPH, self.MORPH ) )
		closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )
		contours, h, _ = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		for cont in h:
			if cv2.contourArea(cont) > 5000:
				arc_len = cv2.arcLength(cont, True)
				approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)

				if ( len( approx ) == 4 ):
					self.IS_FOUND = 1
					#M = cv2.moments( cont )
					#cX = int(M["m10"] / M["m00"])
					#cY = int(M["m01"] / M["m00"])
					#cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

					pts_src = np.array( approx, np.float32 )

					h, status = cv2.findHomography( pts_src, self.pts_dst )
					out = cv2.warpPerspective( rgb, h, ( int( self._width + self._margin * 2 ), int( self._height + self._margin * 2 ) ) )

					cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )

					print("aaaa")
				else : pass

		print("run")
		current = str(time.time())
		#cv2.namedWindow( 'edges', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow('edges', edges)
		#cv2.imwrite("edges_"+current+".jpg", edges)

		#cv2.namedWindow( 'rgb', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow('rgb', rgb)
		#cv2.imwrite("rgb_"+current+".jpg", rgb)

		#if self.IS_FOUND:
		#	#cv2.namedWindow( 'out', cv2.CV_WINDOW_AUTOSIZE )
		#	cv2.imshow('out', out)
		#	#cv2.imwrite("out_"+current+".jpg", out)
		
	def dudu(self, matrice):
		rgb = matrice
	
		gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )

		gray = cv2.bilateralFilter( gray, 1, 10, 120 )

		edges  = cv2.Canny( gray, 10, self.CANNY )

		kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( self.MORPH, self.MORPH ) )

		closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

		contours, h, _ = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		for cont in h:

			if cv2.contourArea ( cont ) > 5000 :

				arc_len = cv2.arcLength( cont, True )

				approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )

				if ( len( approx ) == 4 ):
					self.IS_FOUND = 1
					#M = cv2.moments( cont )
					#cX = int(M["m10"] / M["m00"])
					#cY = int(M["m01"] / M["m00"])
					#cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

					pts_src = np.array( approx, np.float32 )

					h, status = cv2.findHomography( pts_src, self.pts_dst )
					out = cv2.warpPerspective( rgb, h, ( int( self._width + self._margin * 2 ), int( self._height + self._margin * 2 ) ) )

					cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )

				else : pass

		current = str(time.time())
                #cv2.namedWindow( 'edges', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow( 'edges', edges )
		#cv2.imwrite("edges_"+current+".jpg", edges)

		#cv2.namedWindow( 'rgb', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow( 'rgb', rgb )
		#cv2.imwrite("rgb_"+current+".jpg", rgb)

		if self.IS_FOUND :
			#cv2.namedWindow( 'out', cv2.CV_WINDOW_AUTOSIZE )
			cv2.imshow( 'out', out )
			#cv2.imwrite("out_"+current+".jpg", out)
			self.IS_FOUND = 0
		cv2.waitKey(27) & 0xFF == ord('q')