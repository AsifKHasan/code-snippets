#!/usr/bin/env python3

import os
import argparse
import cv2
import numpy as np
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image for preprocessing")
ap.add_argument("-t", "--threshold", required=True, help="threshhold value over which the gray pixels will be treated as background noise to clean the image")
ap.add_argument("-o", "--outprefix", required=True, help="prefix of output image name after preprocessing")
args = vars(ap.parse_args())
thresholdValue = int(args["threshold"])
pre = args["outprefix"]

# load the image
gray = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)

# resize the image let us make width 1920
gray = imutils.resize(gray, width = 1920)

clean = gray.copy()
clean[np.where((clean>=[thresholdValue]))] = [255]

black = clean.copy()
black[np.where((black<[thresholdValue]))] = [0]

# make a clean image by eliminating all light gray pixels valued above and threshold value
th, thresh = cv2.threshold(clean, thresholdValue, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

# denoise the image
# h :
#    Parameter regulating filter strength.
#    Big h value perfectly removes noise but also removes image details,
#    smaller h value preserves details but also preserves some noise
#    Therefore, In order to remove noise, we have to increase filter strength parameter h, big h value perfectly remove noise, but smaller h value preserves details and also preserve some noise.
# templateWindowSize :
#    Size in pixels of the template patch that is used to compute weights.
#    Should be odd. Recommended value 7 pixels
# searchWindowSize :
#    Size in pixels of the window that is used to compute weighted average for given pixel.
#    Should be odd. Affect performance linearly: greater searchWindowsSize - greater denoising time. Recommended value 21 pixels
# nonoise = cv2.fastNlMeansDenoising(gray, None, h=5, templateWindowSize=7, searchWindowSize=21)

# d :
#    Diameter of each pixel neighborhood that is used during filtering. If it is non-positive, it is computed from sigmaSpace .
# sigmaColor :
#    Filter sigma in the color space.
#    A larger value of the parameter means that farther colors within the pixel neighborhood (see sigmaSpace ) will be mixed together, resulting in larger areas of semi-equal color.
# sigmaSpace :
#    Filter sigma in the coordinate space.
#    A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough (see sigmaColor ). When d>0 , it specifies the neighborhood size regardless of sigmaSpace . Otherwise, d is proportional to sigmaSpace .
# filtered = cv2.bilateralFilter(gray, d=-1, sigmaColor=11, sigmaSpace=11)

# create a dilated image
#dilated = nonoise.copy()
#kernel = np.ones((1,1), np.uint8)
#dilated = cv2.dilate(dilated, kernel, iterations = 1)

# blur the black image
#blur = cv2.GaussianBlur(dilated, (3,3), 0)

# apply gaussian and mean adaptive thresholding on the blurred image
kernel = np.ones((1,1), np.uint8)
#mean = cv2.adaptiveThreshold(nonoise, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 2)
#gauss = cv2.adaptiveThreshold(nonoise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 2)

# erode
eroded = cv2.erode(thresh, kernel, iterations = 3)

# dilated
dilated = cv2.erode(thresh, kernel, iterations = 1)

# erode and dilate
open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# dilate and erode
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# detect edges
edged = cv2.Canny(thresh, 100, 200)

# write the grayscale image to disk as a temporary file so we can apply OCR to it
#cv2.imwrite("{}-gray.png".format(pre), gray)
cv2.imwrite("{}-black.png".format(pre), clean)
cv2.imwrite("{}-clean.png".format(pre), clean)
cv2.imwrite("{}-thresh.png".format(pre), thresh)
cv2.imwrite("{}-eroded.png".format(pre), eroded)
cv2.imwrite("{}-dilated.png".format(pre), dilated)
cv2.imwrite("{}-open.png".format(pre), open)
cv2.imwrite("{}-closed.png".format(pre), closed)
cv2.imwrite("{}-edged.png".format(pre), edged)
