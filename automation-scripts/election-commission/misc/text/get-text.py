#!/usr/bin/env python3

import fitz

# PROJ_DIR = "D:/projects/asif@github/code-snippets/automation-scripts/election-commission"
PROJ_DIR = "/home/asif/projects/asif@github/code-snippets/automation-scripts/election-commission"
input_pdf = f"{PROJ_DIR}/data/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.pdf"
output_txt = f"{PROJ_DIR}/out/cleaned/30-Dhaka/93-Tangail/23-Delduar/109-Atia/930138/930138_com_521_female_without_photo_31_2024-3-21.txt"

doc = fitz.open(input_pdf)
page = doc[32]
texts = page.get_text('blocks')
for text in texts:
    if len(text) >= 4:
        byte_array = bytes(text[4], 'utf-8')
        print(byte_array)

lines = [text[4] for text in texts]
with open(output_txt, 'w', encoding="UTF-8") as fh: fh.writelines(lines)
