#!/usr/bin/env python3

from PIL import Image
import pytesseract
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd. Must be in grayscale")
ap.add_argument("-o", "--outprefix", required=True, help="prefix of output file for storing output")
ap.add_argument("-l", "--lang", type=str, default="ben",help="language to be detected")
args = vars(ap.parse_args())

# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
text = pytesseract.image_to_string(Image.open(args["image"]), lang=args["lang"])
with open(args["outprefix"] + ".txt", "a") as f:
	f.write(text)
	f.write("\n")
