#!/usr/bin/env python3

'''
Detect text lines from an image and segment them into separate images
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
args = vars(ap.parse_args())
thresholdValue = int(args["threshold"])
pre = args["outprefix"]

# load the image
image = cv2.imread(args["image"])

## (2) threshold
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
th, threshed = cv2.threshold(gray, thresholdValue, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

## (3) minAreaRect on the nozeros
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx,cy), (w,h), ang = ret
if w>h:
    w,h = h,w
    ang += 90

## (4) Find rotated matrix, do rotation
M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
rotated = cv2.warpAffine(threshed, M, (image.shape[1], image.shape[0]))

## (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)

th = 2
H,W = image.shape[:2]
uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

line = 0
for x in zip(uppers, lowers):
	cropped = gray[x[0]:x[1], 0:W]
	cv2.imwrite("{}-line-{}.png".format(pre, line), cropped)
	line = line + 1

rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
for y in uppers:
    cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)

for y in lowers:
    cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)

# write the images back
cv2.imwrite("{}-gray.png".format(pre), gray)
cv2.imwrite("{}-clean.png".format(pre), threshed)
cv2.imwrite("{}-lined.png".format(pre), rotated)
