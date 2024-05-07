#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, TextStringObject

# The watermark text
wm_text = "চূড়ান্ত ভোটার তালিকা"
replace_with = ""

# Load PDF into pyPDF
reader = PdfReader("C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-original.pdf")
writer = PdfWriter()

# Iterate over the pages in the PDF file
for page in reader.pages:
    blank_page = page.create_blank_page(reader)
    # Remove the watermark 
    page.merge_page(page2=blank_page, over=False)
    # Add the page to the PDFWriter object
    writer.add_page(page)


# Write the stream
with open("C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-wo-watermark.pdf", "wb") as fh:
    writer.write(fh)
