#!/usr/bin/env python3

''' usage
	./text-from-image.py --image page-01
'''

# import required packages
import platform
import argparse

# import easyocr
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

from pprint import pprint


# the installed location of Tesseract-OCR in your system
if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
# PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930119/930119_com_1745_female_without_photo_103_2024-3-21.pdf"
output_txt = f"{PROJ_DIR}/out/voter-cleaned.txt"


IMG_PATH = "{}/out/pages/{}.png"
IMG_OUTPUT_PATH = "{}/out/segments/{}__{}x{}-{}.png"
OCR_OUTPUT_PATH = "{}/out/texts/{}.txt"

SEGMENT_MIN_HEIGHT = 100

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
	img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

	# Preprocessing the image starts

	# Performing OTSU threshold
	thresh, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
	# thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	# img_bin = 255 - img_bin

	# img_bin, kernel, ver_kernel, hor_kernel  = get_kernels(img, img_bin, thresh)
	# vertical_lines = get_vertical_lines(img_bin, ver_kernel)
	# horizontal_lines = get_horizontal_lines(img_bin, hor_kernel)

	# img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
	# img_vh = cv2.addWeighted(vertical_lines, 0.1, horizontal_lines, 0.1, 0.0)
	# img_vh = cv2.erode(~img_vh, kernel, iterations=1)
	# thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	# thresh, img_vh = cv2.threshold(img_vh, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	# bitxor = cv2.bitwise_xor(img,img_vh)
	# bitnot = cv2.bitwise_not(bitxor)

	contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours, bounding_boxes = sort_contours(contours, method="top-to-bottom")

	for c in contours:
		x, y, w, h = cv2.boundingRect(c)
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 1)

	# output_path = IMG_OUTPUT_PATH.format(PROJ_DIR, img_name, 0, 0, 0)
	# cv2.imwrite(output_path, img)

	heights = [bounding_boxes[i][3] for i in range(len(bounding_boxes))]
	mean = np.mean(heights)

	print(f"found {len(contours)} contours")
	boxes = get_list_of_box(img, contours)
	print(f"found {len(boxes)} boxes")
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


def save_image_segments(image_segments, img_name, img_output_path):
	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				y, x, w, h = box['box'][0], box['box'][1], box['box'][2], box['box'][3]

				# remove boxes with less than a specified height
				if h > SEGMENT_MIN_HEIGHT:
					img = box['img']

					# crop to remove black borders
					img = img[9:h-9, 9:w-9]

					# manipulate image
					kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

					# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
					# img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
					# img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255,255])
					# img = cv2.dilate(img, kernel,iterations=1)
					# img = cv2.erode(img, kernel,iterations=1)
					# show_image(img=img)

					# Perform morphological operations to remove noise
					# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
					img = cv2.resize(img, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)

					output_path = img_output_path.format(PROJ_DIR, img_name, row_num, col_num, idx)
					rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
					pil_image = Image.fromarray(rgb_image)
					pil_image.save(output_path, dpi=(600,600))
					box['do-ocr'] = True
					box['img'] = img
	
				else:
					box['do-ocr'] = False


				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1


def ocr_segments_easyocr(image_segments):
	easyocr_reader = easyocr.Reader(['bn'])

	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				if box['do-ocr']:
					img = box['img']

					texts = easyocr_reader.readtext(img, detail=0, paragraph=True)
					text = '\n'.join(texts)
					box['ocr'] = text.strip()

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1


def ocr_segments(image_segments):
	config = '-c preserve_interword_spaces=1 --psm 4 --dpi 600 --oem 3'

	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				if box['do-ocr']:
					img = box['img']

					kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

					# Perform morphological operations to remove noise
					# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
					# img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

					# img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255,255])
					# img = cv2.dilate(img, kernel,iterations=1)
					# img = cv2.erode(img, kernel,iterations=1)
					# show_image(img=img)

					# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
					# img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

					text = pytesseract.image_to_string(img, lang='ben', config=config)
					box['ocr'] = text.strip()

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1


def save_ocr_texts(image_segments, ocr_output_path):
	file = open(ocr_output_path, "w", encoding='utf-8')

	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				if box['do-ocr']:
					ocr_text = box['ocr'].strip()
					ocr_text = ocr_text.replace('\n\n', '\n')
					if ocr_text != "":
						file.write(ocr_text)
						file.write('\n\n')
						print(ocr_text)
						print()

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1

	file.close


def show_image(img):
	image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	plt.imshow(image)
	plt.show()


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="image name to work with", default=argparse.SUPPRESS)
	args = vars(ap.parse_args())

	img_name = args['image']
	img_path = IMG_PATH.format(PROJ_DIR, img_name)
	ocr_output_path = OCR_OUTPUT_PATH.format(PROJ_DIR, img_name)

	image_segments = segment_image(image_path=img_path, no_segmentation=False)
	save_image_segments(image_segments=image_segments, img_name=img_name, img_output_path=IMG_OUTPUT_PATH)
	# ocr_segments(image_segments=image_segments)
	# ocr_segments_easyocr(image_segments=image_segments)
	# save_ocr_texts(image_segments=image_segments, ocr_output_path=ocr_output_path)
