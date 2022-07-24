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

IMG_NAME = "faq-06"
IMG_PATH = f"./data/ibas/ibas-faq/{IMG_NAME}.png"
IMG_OUTPUT_PATH = "./out/{}x{}-{}.png"
OCR_OUTPUT_PATH = f"./out/{IMG_NAME}.txt"

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


def get_horizontal_lines(img_bin,hor_kernel):
	image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
	horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

	return horizontal_lines


def get_list_of_box(img, contours):
	boxes = []
	# img_height, *_ = img.shape
	img_height = 1000

	for c in contours:
		x, y, w, h = cv2.boundingRect(c)

		if (20 < h < img_height):
			image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
			cropped = img[y:y+h, x:x+w]
			# cv2_imshow(crop_img)

			boxes.append({'img': cropped, 'box': [x, y, w, h]})

	return boxes


def get_row_and_columns(boxes, mean):
	rows = []
	cols = []
	j = 0

	for i in range(len(boxes)):
		if (i == 0):
			cols.append(boxes[i])
			previous = boxes[i]
		else:
			if (boxes[i]['box'][1] <= previous['box'][1] + mean / 2):
				cols.append(boxes[i])
				previous = boxes[i]
				if (i == len(boxes) - 1):
					rows.append(cols)
			else:
				rows.append(cols)
				cols = []
				previous = boxes[i]
				cols.append(boxes[i])

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
			diff = abs(center- (row[i][j]['box'][0] + row[i][j]['box'][2] / 4))
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

	# print(f"found {len(contours)} contours")
	boxes = get_list_of_box(bitnot, contours)
	# print(f"found {len(boxes)} boxes")
	rows, cols = get_row_and_columns(boxes, mean)

	num_cols = 0
	for i in range(len(rows)):
		count = len(rows[i])
		if count > num_cols:
			num_cols = count

	center = [int(rows[i][j]['box'][0] + rows[i][j]['box'][2] / 2) for j in range(len(rows[i])) if rows[0]]
	center = np.array(center)
	center.sort()
	final_boxes = arrange_boxes_in_order(rows, num_cols, center)

	return final_boxes


def save_image_segments(image_segments, img_output_path):
	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				y, x, w, h = box['box'][0], box['box'][1], box['box'][2], box['box'][3]
				output_path = img_output_path.format(row_num, col_num, idx)
				cv2.imwrite(output_path, box['img'])

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1


def ocr_segments(image_segments):
	# config = '-c preserve_interword_spaces=1 --psm 4 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 6 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 11 --oem 3'
	# config = '-c preserve_interword_spaces=1 --psm 12 --oem 3'
	config = '-c preserve_interword_spaces=1 --oem 3'

	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
				border = cv2.copyMakeBorder(box['img'], 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255,255])
				resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
				dilation = cv2.dilate(resizing, kernel,iterations=1)
				erosion = cv2.erode(dilation, kernel,iterations=1)

				text = pytesseract.image_to_string(erosion, lang='eng+ben', config=config)
				# text = pytesseract.image_to_pdf_or_hocr(box['img'], lang='eng+ben', config=config, extension='hocr')
				# text = pytesseract.run_and_get_output(box['img'], lang='eng+ben', config=config, extension='hocr')

				box['ocr'] = text.strip()

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1


def save_ocr_texts(image_segments, ocr_output_path):
	file = open(OCR_OUTPUT_PATH, "w")

	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				file.write(f"{row_num}x{col_num}-{idx}")
				file.write("\n")
				file.write(box['ocr'])
				file.write("\n")

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1

	file.close


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with", default=argparse.SUPPRESS)
    # args = vars(ap.parse_args())

	image_segments = segment_image(image_path=IMG_PATH, no_segmentation=True)
	save_image_segments(image_segments=image_segments, img_output_path=IMG_OUTPUT_PATH)
	ocr_segments(image_segments=image_segments)
	save_ocr_texts(image_segments=image_segments, ocr_output_path=OCR_OUTPUT_PATH)
