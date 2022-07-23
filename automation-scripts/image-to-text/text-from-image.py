#!/usr/bin/env python3

# import required packages
import platform
import argparse

import cv2
import numpy as np
import pytesseract

from pprint import pprint


# the installed location of Tesseract-OCR in your system
if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


IMG_PATH = "./data/ibas/ibas-faq/faq-01.png"
IMG_OUTPUT_PATH = "./out/{}x{}-{}.png"
OCR_OUTPUT_PATH = "./out/{}.html"
PARSED_OUTPUT_PATH = "./out/{}.txt"

def get_kernels(img, img_bin, thresh):
	kernel_len = np.array(img).shape[1]//100
	ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
	hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

	return img_bin, kernel,  ver_kernel, hor_kernel


def get_vertical_lines(img_bin,ver_kernel):
	image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
	vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

	return vertical_lines


#@title Apply Horizontal Kernels
def get_horizontal_lines(img_bin,hor_kernel):
	image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
	horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

	return horizontal_lines


#@title Get the List of Boxes
def get_list_of_box(img,contours):
	box = []

	for c in contours:
		x, y, w, h = cv2.boundingRect(c)

		if (20 < h < 2000):
			image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
			crop_img = img[y:y+h, x:x+w]
			# cv2_imshow(crop_img)

			box.append([x, y, w, h])

	return box


def get_row_and_columns(box, mean):
	rows = []
	cols = []
	j = 0

	for i in range(len(box)):
		if(i == 0):
		  cols.append(box[i])
		  previous = box[i]
		else:
			if(box[i][1] <= previous[1] + mean / 2):
				cols.append(box[i])
				previous = box[i]
				if (i == len(box) - 1):
					rows.append(cols)
			else:
				rows.append(cols)
				cols = []
				previous = box[i]
				cols.append(box[i])

	return rows, cols


def sort_contours(cnts, method="left-to-right"):
	reverse = False
	i = 0

	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True

	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	bounding_boxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, bounding_boxes) = zip(*sorted(zip(cnts, bounding_boxes), key = lambda b:b[1][i], reverse=reverse))

	return (cnts, bounding_boxes)


def arrange_boxes_in_order(row, countcol, center):
	final_boxes = []

	for i in range(len(row)):
		lis = []
		for k in range(countcol):
			lis.append([])

		for j in range(len(row[i])):
			diff = abs(center- (row[i][j][0] + row[i][j][2] / 4))
			minimum = min(diff)
			indexing = list(diff).index(minimum)
			lis[indexing].append(row[i][j])

		final_boxes.append(lis)

	return final_boxes


def segment_image(image_path, no_segmentation=False):
	# Read image from which text needs to be extracted
	img = cv2.imread(image_path, 0)

	# Preprocessing the image starts

	# Convert the image to gray scale
	# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Performing OTSU threshold
	# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
	thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	img_bin = 255 - img_bin

	img_bin, kernel, ver_kernel, hor_kernel  = get_kernels(img, img_bin, thresh)
	vertical_lines = get_vertical_lines(img_bin, ver_kernel)
	horizontal_lines = get_horizontal_lines(img_bin, hor_kernel)

	img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
	img_vh = cv2.erode(~img_vh, kernel, iterations=2)
	thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	bitxor = cv2.bitwise_xor(img,img_vh)
	bitnot = cv2.bitwise_not(bitxor)

	contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours, bounding_boxes = sort_contours(contours, method="top-to-bottom")

	heights = [bounding_boxes[i][3] for i in range(len(bounding_boxes))]
	mean = np.mean(heights)

	box = get_list_of_box(img, contours)
	rows, cols = get_row_and_columns(box, mean)

	num_cols = 0
	for i in range(len(rows)):
		count = len(rows[i])
		if count > num_cols:
			num_cols = count

	center = [int(rows[i][j][0] + rows[i][j][2] / 2) for j in range(len(rows[i])) if rows[0]]
	center = np.array(center)
	center.sort()
	final_boxes = arrange_boxes_in_order(rows, num_cols, center)

	return bitnot, final_boxes







	# Specify structure shape and kernel size.
	# Kernel size increases or decreases the area
	# of the rectangle to be detected.
	# A smaller value like (10, 10) will detect
	# each word instead of a sentence.
	# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

	# Applying dilation on the threshold image
	# dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

	# if no_segmentation:
	# 	return [(img, 0, None)]

	# Finding contours
	# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Looping through the identified contours
	# Then rectangular part is cropped
	# image_segments = []
	# i = 0
	# for cnt in contours:
	# 	x, y, w, h = cv2.boundingRect(cnt)
	#
	# 	# Drawing a rectangle on copied image
	# 	rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
	#
	# 	# Cropping the text block for giving input to OCR
	# 	cropped = im2[y:y + h, x:x + w]
	#
	# 	image_segments.append((cropped, i, (x, y, w, h)))
	#
	# 	i = i + 1
	#
	# return image_segments


def save_image_segments(img, image_segments, img_output_path):
	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				y, x, w, h = box[0], box[1], box[2], box[3]
				cropped = img[x:x+h, y:y+w]
				output_path = img_output_path.format(row_num, col_num, idx)
				cv2.imwrite(output_path, cropped)

			col_num = col_num + 1

		row_num = row_num + 1


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

	img, image_segments = segment_image(image_path=IMG_PATH, no_segmentation=True)
	# pprint(image_segments)
	save_image_segments(img=img, image_segments=image_segments, img_output_path=IMG_OUTPUT_PATH)
	# ocr_texts = ocr_segments(image_segments=image_segments)
	# save_ocr_texts(ocr_texts=ocr_texts, ocr_output_path=OCR_OUTPUT_PATH)
	# parse_ocr_texts(ocr_texts=ocr_texts, parsed_output_path=PARSED_OUTPUT_PATH)
