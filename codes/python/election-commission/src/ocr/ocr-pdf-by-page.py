#!/usr/bin/env python3

import fitz
import ocrmypdf
import sys
import io

PROJ_DIR = '..'
input_pdf = f"{PROJ_DIR}/out/voter-cleaned.pdf"
output_txt = f"{PROJ_DIR}/out/voter-cleaned.txt"

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
        language="eng+ben",  # modify as required e.g. ("eng", "ger")
        output_type="pdf",  # only need simple PDF format
        # add more paramneters, e.g. to enforce OCR-ing, etc., e.g.
        # force_ocr=True, redo_ocr=True
    )
    ocr_pdf = fitz.open("pdf", outbytes.getvalue())  # read output as fitz PDF
    text = ocr_pdf[0].get_text()  # ...and extract text from the page
    return text  # return it


if __name__ == "__main__":
    doc = fitz.open(input_pdf)
    for page in doc:
        text = ocr_the_page(page)
        with open(output_txt, 'w', encoding="UTF-8") as fh:
            fh.writelines(text)
