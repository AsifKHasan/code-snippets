#!/usr/bin/env python3

import fitz
import easyocr
import time

PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
# PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930119/930119_com_1745_female_without_photo_103_2024-3-21.pdf"
output_txt = f"{PROJ_DIR}/out/voter-cleaned.txt"

easyocr_reader = easyocr.Reader(["en"])

mat = fitz.Matrix(4, 4)  # high resolution matrix
ocr_time = 0
pix_time = 0


def get_easyocr(page, bbox):
    """Return OCR-ed span text using Tesseract.

    Args:
        page: fitz.Page
        bbox: fitz.Rect or its tuple
    Returns:
        The OCR-ed text of the bbox.
    """
    global mat, ocr_time, pix_time
    # Step 1: Make a high-resolution image of the bbox.
    t0 = time.perf_counter()
    pix = page.get_pixmap(
        colorspace=fitz.csGRAY,
        matrix=mat,
        clip=bbox,
    )
    image = pix.tobytes("png")
    t1 = time.perf_counter()

    # Step 2: Invoke easyocr to OCR the image.
    detected_text = easyocr_reader.readtext(
        image,
        detail=0,
    )
    t2 = time.perf_counter()
    ocr_time += t2 - t1
    pix_time += t1 - t0
    if len(detected_text) > 0:
        return detected_text[0]
    else:
        return "*** could not interpret ***"


doc = fitz.open(input_pdf)
ocr_count = 0
texts = []
for page in doc:
    print(page)
    page_dict = page.get_text("dict")
    print(page_dict)
    text_blocks = page_dict["blocks"]
    for b in text_blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                ocr_count += 1
                print("before: '%s'" % text)
                new_text = get_easyocr(page, s["bbox"])
                print(new_text)

print("-------------------------")
print("OCR invocations: %i." % ocr_count)
# print("Pixmap time: %g (avg %g) seconds." % (round(pix_time, 5), round(pix_time / ocr_count, 5)))
# print("OCR time: %g (avg %g) seconds." % (round(ocr_time, 5), round(ocr_time / ocr_count, 5)))
