#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, TextStringObject

PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
# PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930119/930119_com_1745_female_without_photo_103_2024-3-21.pdf"
output_pdf = f"{PROJ_DIR}/out/cleaned/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930119/930119_com_1745_female_without_photo_103_2024-3-21.pdf"

# The watermark text
wm_text = "চূড়ান্ত ভোটার তালিকা"
replace_with = ""

# Load PDF into pyPDF
reader = PdfReader(input_pdf)
writer = PdfWriter()

# Iterate over the pages in the PDF file
for page in reader.pages:
    blank_page = page.create_blank_page(reader)
    # Remove the watermark 
    page.merge_page(page2=blank_page, over=False)
    # Add the page to the PDFWriter object
    writer.add_page(page)


# Write the stream
with open(output_pdf, 'wb') as fh:
    writer.write(fh)
