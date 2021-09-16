#!/usr/bin/env python3

'''
Segmentize an image of NID card into at least two recangular block,
* one containing the header part and
* one containing the information part
'''

import os
import argparse
import cv2
import numpy as np
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image for preprocessing")
ap.add_argument("-o", "--outprefix", required=True, help="prefix of output image name after preprocessing")
ap.add_argument("-t", "--threshold", required=True, help="threshhold value over which the gray pixels will be treated as background noise to clean the image")
ap.add_argument("-p", "--epsilonpct", required=True, help="% of arc length for rectangular edge contour approximation")
ap.add_argument("-m", "--morphpixels", required=True, help="pixels to make kernel for elipsoid morphing")
args = vars(ap.parse_args())
thresholdValue = int(args["threshold"])
epsilonpct = float(args["epsilonpct"])
morphpixels = int(args["morphpixels"])
pre = args["outprefix"]

# load the image
image = cv2.imread(args["image"])

# resize the image let us make width 1920
image = imutils.resize(image, width = 1920)

# convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 11, 11)

# make a clean image by eliminating all light gray pixels valued above and threshold value
clean = gray.copy()
clean[np.where((clean>=[thresholdValue]))] = [255]

# make all remaining pixels more black than 180 to full black
ret,black = cv2.threshold(clean, thresholdValue, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

# Connect the lines in the border is using morphological operators. Merge the lines that are close and fill some of the empty spaces
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morphpixels, morphpixels))
edged = cv2.dilate(black, kernel)

# detect edges
edged = cv2.Canny(edged, 100, 200)

# find contours in the edged image, keep only the largest ones, and initialize our screen contour
_, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("{} edge contour(s) found".format(len(cnts)))
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

screenCnt = []
# loop over our contours to find out rectabgular big blocks
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	epsilon = (epsilonpct / 100) * peri
	approx = cv2.approxPolyDP(c, epsilon, True)

	# if our approximated contour has four points, then we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt.append(approx)

print("{} major rectangular block(s) found".format(len(screenCnt)))

# now draw recangles over the findContours
cropCount = 0
for c in screenCnt:
	# get the bounding rectangle of the countour
	x,y,w,h = cv2.boundingRect(c)
	#cv2.rectangle(clean, (x,y), (x+w, y+h), (0,255,0), 2)
	cropped = gray[y:y+h, x:x+w]
	fn = "{}-s{}-m{}-e{}.png".format(pre, cropCount, morphpixels, epsilonpct)
	cv2.imwrite(fn, cropped)
	print("segment {} cropped in : {}".format(cropCount, fn))
	cropCount = cropCount + 1
    #cv2.drawContours(clean, [c], -1, (0, 255, 0), 3)

print("{} segment(s) cropped".format(cropCount))

# write the images back
cv2.imwrite("{}-gray.png".format(pre), gray)
#cv2.imwrite("{}-edged.png".format(pre), edged)
#cv2.imwrite("{}-black.png".format(pre), black)
#cv2.imwrite("{}-clean.png".format(pre), clean)
