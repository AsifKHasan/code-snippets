#!/usr/bin/env python3

# import required packages
import platform
import argparse

import cv2
import pytesseract
from bs4 import BeautifulSoup


# the installed location of Tesseract-OCR in your system
if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


IMG_PATH = "./data/ibas/ibas-faq/faq-01.png"
IMG_OUTPUT_PATH = "./out/{}.png"
OCR_OUTPUT_PATH = "./out/{}.html"
PARSED_OUTPUT_PATH = "./out/{}.txt"

def segment_image(image_path, no_segmentation=False):
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

	if no_segmentation:
		return [(img, 0, None)]

	# Finding contours
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Looping through the identified contours
	# Then rectangular part is cropped
	image_segments = []
	i = 0
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		
		# Drawing a rectangle on copied image
		rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		# Cropping the text block for giving input to OCR
		cropped = im2[y:y + h, x:x + w]

		image_segments.append((cropped, i, (x, y, w, h)))

		i = i + 1

	return image_segments


def save_image_segments(image_segments, img_output_path):
	for image_segment in image_segments:
		img = image_segment[0]
		output_path = img_output_path.format(f"{image_segment[1]:03}")
		cv2.imwrite(output_path, img)


def ocr_segments(image_segments):
	# Apply OCR on the cropped images
	# config = '-c preserve_interword_spaces=1 --psm 4 --oem 3'
	config = '-c preserve_interword_spaces=1 --psm 6 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 11 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 12 --oem 3'

	ocr_texts = []
	for image_segment in image_segments:
		img = image_segment[0]
		# text = pytesseract.image_to_string(img, lang='eng+ben', config=config)
		# text = pytesseract.image_to_pdf_or_hocr(img, lang='eng+ben', config=config, extension='hocr')
		text = pytesseract.run_and_get_output(img, lang='eng+ben', config=config, extension='hocr')
	
		# Appending the text into file
		ocr_texts.append((text, image_segment[1]))

	return ocr_texts


def save_ocr_texts(ocr_texts, ocr_output_path):
	for ocr_text in ocr_texts:
		# Open the file in append mode
		file = open(ocr_output_path.format(f"{ocr_text[1]:03}"), "a")

		# Appending the text into file
		file.write(ocr_text[0])
		file.write("\n")
	
		# Close the file
		file.close


def parse_ocr_texts(ocr_texts, parsed_output_path):
	for ocr_text in ocr_texts:
		# Open the file in append mode
		file = open(parsed_output_path.format(f"{ocr_text[1]:03}"), "a")

		text = ocr_text[0]

		soup = BeautifulSoup(text)
		
	
		# Close the file
		file.close


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with", default=argparse.SUPPRESS)
    # args = vars(ap.parse_args())

	image_segments = segment_image(image_path=IMG_PATH, no_segmentation=True)
	save_image_segments(image_segments=image_segments, img_output_path=IMG_OUTPUT_PATH)
	ocr_texts = ocr_segments(image_segments=image_segments)
	save_ocr_texts(ocr_texts=ocr_texts, ocr_output_path=OCR_OUTPUT_PATH)
	parse_ocr_texts(ocr_texts=ocr_texts, parsed_output_path=PARSED_OUTPUT_PATH)
