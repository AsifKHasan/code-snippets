#!/usr/bin/env python3

import io
import fitz
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageOps

# import pymupdf
# import pprint
# import easyocr
# import ocrmypdf

from helper.logger import *


# high resolution matrix
mat = fitz.Matrix(2, 2)

def ocr_the_page(page):
    """Extract the text from passed-in PDF page."""
    src = page.parent  # the page's document
    doc = fitz.open()  # make temporary 1-pager
    doc.insert_pdf(src, from_page=page.number, to_page=page.number)
    pdfbytes = doc.tobytes()
    inbytes = io.BytesIO(pdfbytes)  # transform to BytesIO object
    outbytes = io.BytesIO()  # let ocrmypdf store its result pdf here
    ocrmypdf.ocr(
        inbytes,  # input 1-pager
        outbytes,  # ouput 1-pager
        # image_dpi=600,
        language="ben",  # modify as required e.g. ("eng", "ger")
        output_type="pdf",  # only need simple PDF format
        # add more paramneters, e.g. to enforce OCR-ing, etc., e.g.
        force_ocr=True,
        clean=True,
        # remove_background=True,
        progress_bar=False,
        # oversample=600,
    )
    ocr_pdf = fitz.open("pdf", outbytes.getvalue())  # read output as fitz PDF
    text = ocr_pdf[0].get_text()  # ...and extract text from the page
    return text  # return it



'''
'''
def page_text_tesseract(image_file, dpi=600, psm=4, oem=3):
    config = f"-c preserve_interword_spaces=1 --dpi {dpi} --psm {psm} --oem {oem}"
    # config = f"-c preserve_interword_spaces=1"

    image = cv2.imread(image_file)

    # TODO: make resize work
    # image = cv2.resize(image, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)


    # TODO: undersatnd what is getting changed through this
    # Convert to grayscale, apply Gaussian blur, and threshold
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove noise using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    image = 255 - image

    text = pytesseract.image_to_string(image, lang='ben', config=config)
    # text = pytesseract.image_to_string(image, lang='ben')

    return text



'''
'''
def page_text_easyocr(pdf_file, page_num):
    global mat
    easyocr_reader = easyocr.Reader(['bn'])

    # open input
    doc = fitz.open(pdf_file)

    page = doc[page_num]
    pix = page.get_pixmap(colorspace=fitz.csGRAY, matrix=mat)
    img = pix.tobytes("png")

    texts = easyocr_reader.readtext(img, detail=0, paragraph=True)
    text = '\n'.join(texts)

    return text



'''
'''
def page_text_mupdf(image_file):

    doc = fitz.open()
    pix = fitz.Pixmap(image_file)
    imgpdf = fitz.open("pdf", pix.pdfocr_tobytes())
    doc.insert_pdf(imgpdf)
    pix = None
    page = doc[0]
    # texts = page.get_text('html')
    text_page = page.get_textpage_ocr(flags=3, language='ben', dpi=500, full=True)
    texts = text_page.extractText(sort=True)

    # texts = ocr_the_page(page)


    # open input
    # pix = Pixmap(image_file)
    # doc = fitz.open(pdf_file)

    # page = doc[page_num]
    # texts = page.get_text('html')
    # text_page = page.get_textpage_ocr(flags=3, language='ben', dpi=300, full=True)
    # texts = text_page.extractText(sort=True)

    # texts = ocr_the_page(page)
    
    return texts
            


'''
'''
def img_replace(page, xref, filename=None, stream=None, pixmap=None):
    """Replace image identified by xref.

    Args:
        page: a fitz.Page object
        xref: cross reference number of image to replace
        filename, stream, pixmap: must be given as for
        page.insert_image().

    """
    if bool(filename) + bool(stream) + bool(pixmap) != 1:
        raise ValueError("Exactly one of filename/stream/pixmap must be given")
    doc = page.parent  # the owning document
    # insert new image anywhere in page
    new_xref = page.insert_image(
        page.rect, filename=filename, stream=stream, pixmap=pixmap
    )
    doc.xref_copy(new_xref, xref)  # copy over new to old
    last_contents_xref = page.get_contents()[-1]
    # new image insertion has created a new /Contents source,
    # which we will set to spaces now
    doc.update_stream(last_contents_xref, b" ")



''' clear watermark and save pdf pages as image
'''
def clean_and_pagify(input_pdf, output_img_folder, no_page_saving=False, clean_images=False, watermark_is_image=True, dpi=300, first_page_dpi=600):
    
    # open input
    doc = fitz.open(input_pdf)

    if no_page_saving:
        return len(doc)

    if clean_images:
        for page in doc:
            images = page.get_images()  
            for item in images:
                item = images[0]
                old_xref = item[0]

                pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 1, 1), 1)
                pix.clear_with()
                img_replace(page, old_xref, pixmap=pix)


    if watermark_is_image:
        wm_text = b'\x00/\x00O\x00Y\x00K\x01"\x00\x03\x00\xcf\x00A\x00K\x004\x00K\x00D\x00\x03\x009\x00K\x00L\x00E\x00*\x00K'
        # remove all images in all pages
        for page in doc:
            images = page.get_images()  
            for item in images:
                item = images[0]
                old_xref = item[0]

                pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 1, 1), 1)
                pix.clear_with()
                img_replace(page, old_xref, pixmap=pix)

        # remove first two pages
        l = [0] + list(range(2, doc.page_count))
        doc.select(l)

        # save output
        doc.ez_save(output_pdf, garbage=4)

    else:
        wm_text = b'002f004f0059004b0122000300cf0041004b0034004b004400030039004b004c0045002a004b'
        replace_with = b''

        # remove text
        for page in doc:
            for xref in page.get_contents():
                stream = doc.xref_stream(xref)
                stream = stream.replace(wm_text, replace_with)
                doc.update_stream(xref, stream)

            # save as image
            if page.number == 0:
                pix = page.get_pixmap(dpi=first_page_dpi)
            else:
                pix = page.get_pixmap(dpi=dpi)

            pix.save(f"{output_img_folder}/page-{page.number:03d}.png")        

    return len(doc)

        # remove second page
        # l = [0] + list(range(2, doc.page_count))
        # doc.select(l)

        # save output
        # doc.ez_save(output_pdf, garbage=4)

    # else:
    #     reader = PdfReader(input_pdf)
    #     writer = PdfWriter()

    #     l = [0] + list(range(2, len(reader.pages)))
    #     for p in l:
    #         page = reader.pages[p]

    #         # Get the current page's contents
    #         content_object = page["/Contents"]
    #         content = ContentStream(content_object, reader)

    #         # Loop over all pdf elements
    #         for operands, operator in content.operations:
    #             # Was told to adapt this part dependent on my PDF file
    #             if operator == b"Tj":
    #                 if len(operands) and operands[0] == wm_text:
    #                     operands[0] = TextStringObject("")

    #         # Set the modified content as content object on the page
    #         page.__setitem__(NameObject("/Contents"), content)

    #         # Add the page to the output
    #         writer.add_page(page)

    #     # Write the stream
    #     with open(output_pdf, 'wb') as fh:
    #         writer.write(fh)



SEGMENT_MIN_HEIGHT = 100

'''
'''
def get_kernels(img, img_bin, thresh):
	kernel_len = np.array(img).shape[1]//100
	ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
	hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

	return img_bin, kernel,  ver_kernel, hor_kernel



'''
'''
def get_vertical_lines(img_bin,ver_kernel):
	image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
	vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

	return vertical_lines



'''
'''
def get_horizontal_lines(img_bin,hor_kernel):
	image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
	horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

	return horizontal_lines



'''
'''
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



'''
'''
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



'''
'''
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



'''
'''
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



'''
'''
def segment_image(page_image_path, no_segmentation=False, nesting_level=0):
	# Read image from which text needs to be extracted
	img = cv2.imread(page_image_path, cv2.IMREAD_GRAYSCALE)

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

	debug(f"found {len(contours)} contours", nesting_level=nesting_level)
	boxes = get_list_of_box(img, contours)
	debug(f"found {len(boxes)} boxes", nesting_level=nesting_level)
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



'''
'''
def save_image_segments(image_segments, page_image_path, page_image_name, segment_output_directory, segment_min_height=3500, dpi=600, nesting_level=0):
	crop_left_by = 5
	crop_right_by = 5
	crop_top_by = 5
	crop_bottom_by = 5
	resize_x_by = 2
	resize_y_by = 2
	border_xy = 10

    # open the page image
	page_img = Image.open(page_image_path)

	count_saved = 0
	row_num = 1
	for row in image_segments:
		col_num = 1
		for col in row:
			idx = 1
			for box in col:
				x, y, w, h = box['box'][0], box['box'][1], box['box'][2], box['box'][3]
                

				# remove boxes with less than a specified height
				segment_name = f"{page_image_name}__{row_num}x{col_num}-{idx:02d}"
				segment_output_path = f"{segment_output_directory}/{segment_name}.png"
				if h > segment_min_height:
					# crop for segments
					left = x + crop_left_by
					top = y + crop_top_by
					right = left + w - crop_left_by - crop_right_by
					bottom = top + h - crop_top_by - crop_bottom_by
					segment_img = page_img.crop((left, top, right, bottom))

                    # extend image by adding white border
					segment_img = ImageOps.expand(segment_img, border=border_xy, fill='white')

					# segment_img.save(segment_output_path, dpi=(dpi,dpi))
					segment_img.save(segment_output_path)
					debug(f"segment [{segment_name}] saved, height [{h}]", nesting_level=nesting_level)

					count_saved = count_saved + 1
	
				else:
					# debug(f"segment [{segment_name}] ignored, height [{h}]is less than allowed [{segment_min_height}]", nesting_level=nesting_level)
					pass

				idx = idx + 1

			col_num = col_num + 1

		row_num = row_num + 1

	return count_saved



