#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, TextStringObject

# The watermark text
wm_text = "চূড়ান্ত ভোটার তালিকা"
replace_with = ""

# Load PDF into pyPDF
reader = PdfReader("C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-original.pdf")
writer = PdfWriter()

for page in reader.pages:
    # Get the current page's contents
    content_object = page["/Contents"]
    content = ContentStream(content_object, reader)

    # Loop over all pdf elements
    for operands, operator in content.operations:
        # print(operator)

        # Was told to adapt this part dependent on my PDF file
        if operator == b"Tj":
            text = operands[0]
            print(text)
            # if isinstance(text, TextStringObject) and text.startswith(wm_text):
            if isinstance(text, TextStringObject):
                operands[0] = TextStringObject(replace_with)

    # Set the modified content as content object on the page
    page.__setitem__(NameObject("/Contents"), content)

    # Add the page to the output
    writer.add_page(page)

# Write the stream
with open("C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-wo-watermark.pdf", "wb") as fh:
    writer.write(fh)
