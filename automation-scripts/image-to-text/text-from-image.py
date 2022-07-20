#!/usr/bin/env python3

# import required packages
import platform
import argparse

import cv2
import pytesseract


# the installed location of Tesseract-OCR in your system
if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


IMG_PATH = "./data/ibas/ibas-faq/faq-01.png"
OCR_OUTPUT_PATH = "./data/recognized.txt"
IMG_OUTPUT_FOLDER = "./out/"

def segment_image(image_path):
	# Read image from which text needs to be extracted
	img = cv2.imread(image_path)

	# Preprocessing the image starts

	# Convert the image to gray scale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Performing OTSU threshold
	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

	# Specify structure shape and kernel size.
	# Kernel size increases or decreases the area
	# of the rectangle to be detected.
	# A smaller value like (10, 10) will detect
	# each word instead of a sentence.
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

	# Applying dilation on the threshold image
	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

	# Finding contours
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Creating a copy of image
	im2 = img.copy()

	# A text file is created and flushed
	# file = open("./data/recognized.txt", "w+")
	# file.write("")
	# file.close()

	# Looping through the identified contours
	# Then rectangular part is cropped and passed on
	# to pytesseract for extracting text from it
	# Extracted text is then written into the text file
	image_segments = []
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		
		# Drawing a rectangle on copied image
		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		# Cropping the text block for giving input to OCR
		cropped = im2[y:y + h, x:x + w]

		image_segments.append((cropped, (x, y, w, h)))

	return image_segments


def save_image_segments(image_segments, output_folder):
	i = 0
	for image_segment in image_segments:
		img = image_segment[0]
		output_path = f"{output_folder}/{i:03}.png"
		cv2.imwrite(output_path, img)
		i = i + 1


def ocr_segments(image_segments, ocr_output_path):
	# Open the file in append mode
	file = open(ocr_output_path, "a")
	
	# Apply OCR on the cropped images
	# config = '-c preserve_interword_spaces=1 --psm 4 --oem 3'
	config = '-c preserve_interword_spaces=1 --psm 6 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 11 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 12 --oem 3'

	for image_segment in image_segments:
		cropped = image_segment[0]
		# text = pytesseract.image_to_string(cropped, lang='eng+ben', config=config)
		# text = pytesseract.image_to_pdf_or_hocr(cropped, lang='eng+ben', config=config, extension='hocr')
		text = pytesseract.run_and_get_output (cropped, lang='eng+ben', config=config, extension='hocr')
	
		# Appending the text into file
		file.write(text)
		file.write("\n")
	
	# Close the file
	file.close


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with", default=argparse.SUPPRESS)
    # args = vars(ap.parse_args())

	image_segments = segment_image(image_path=IMG_PATH)
	save_image_segments(image_segments=image_segments, output_folder=IMG_OUTPUT_FOLDER)
	# ocr_segments(image_segments=image_segments, ocr_output_path=OCR_OUTPUT_PATH)