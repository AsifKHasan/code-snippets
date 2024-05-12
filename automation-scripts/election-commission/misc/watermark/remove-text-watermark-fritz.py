#!/usr/bin/env python3

import fitz
import binascii
import pprint

# PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.pdf"
output_pdf = f"{PROJ_DIR}/out/cleaned/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.pdf"

# The watermark text
# wm_text = b'\nET\nQ\nQ\nQ\nq\nBT\n/F1'
wm_text = b'002f004f0059004b0122000300cf0041004b0034004b004400030039004b004c0045002a004b'
# wm_text = b'\x00/\x00O\x00Y\x00K\x01"\x00\x03\x00\xcf\x00A\x00K\x004\x00K\x00D\x00\x03\x009\x00K\x00L\x00E\x00*\x00K'
# wm_text = b'\xe0\xa6\x9a\xe0\xa7\x82\xe0\xa7\x9c\xe0\xa6\xbe\xc4\xa2 \xc3\x8f\xe0\xa6\xad\xe0\xa6\xbe\xe0\xa6\x9f\xe0\xa6\xbe\xe0\xa6\xb0 \xe0\xa6\xa4\xe0\xa6\xbe\xe0\xa6\xbf\xe0\xa6\xb2\xe0\xa6\x95\xe0\xa6\xbe'
# wm_text = b'\xe0\xa6\x9a\xe0\xa7\x82\xe0\xa7\x9c\xe0\xa6\xbe\xc4\xa2'
replace_with = b''

# wm_text = bytes.fromhex(wm_text).decode(encoding="Latin1")
# print(wm_text)
# wm_text = binascii.unhexlify(wm_text)

# open input
doc = fitz.open(input_pdf)

for page in doc[32:33]:
    # pprint.pprint(doc.xref_get_keys(page.xref))
    # pprint.pprint(doc.xref_get_key(page.xref, "Content"))
    # print(doc.xref_object(page.xref))
    # exit()
    # xref = page.get_contents()[0]
    # for xref in [xref]:
    # print(page.get_contents())
    for xref in page.get_contents():
        stream = doc.xref_stream(xref)
        # print(stream)
        # print()
        stream = stream.replace(wm_text, replace_with)
        doc.update_stream(xref, stream)

# remove first two pages
l = [0] + list(range(2, doc.page_count))
l = [32]
doc.select(l)

# save output
doc.ez_save(output_pdf, garbage=4)
