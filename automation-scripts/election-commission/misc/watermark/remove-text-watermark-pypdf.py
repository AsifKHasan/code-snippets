#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, TextStringObject

PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
# PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.pdf"
output_pdf = f"{PROJ_DIR}/out/cleaned/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.pdf"

# The watermark text
wm_text = "তািলকা"
wm_text = b'\x00/\x00O\x00Y\x00K\x01"\x00\x03\x00\xcf\x00A\x00K\x004\x00K\x00D\x00\x03\x009\x00K\x00L\x00E\x00*\x00K'
replace_with = ""

# Load PDF into pyPDF
reader = PdfReader(input_pdf)
writer = PdfWriter()

l = [0] + list(range(2, len(reader.pages)))
for p in l:
    page = reader.pages[p]
    # Get the current page's contents
    content_object = page["/Contents"]
    content = ContentStream(content_object, reader)

    # Loop over all pdf elements
    for operands, operator in content.operations:
        # print(operator)

        # Was told to adapt this part dependent on my PDF file
        if operator == b"Tj":
        # if True:
            print(operator)
            # text = operands[0]
            for operand in operands:
                print(operand)
                pass

            print()

            # if isinstance(text, TextStringObject) and text.startswith(wm_text):
            # if isinstance(text, TextStringObject):
            if operands[0] == wm_text:
            # if True:
                # print(text)
                operands[0] = TextStringObject("")
                pass

    # Set the modified content as content object on the page
    page.__setitem__(NameObject("/Contents"), content)

    # Add the page to the output
    writer.add_page(page)

# Write the stream
with open(output_pdf, 'wb') as fh:
    writer.write(fh)
