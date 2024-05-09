#!/usr/bin/env python3

import fitz

PROJ_DIR = "../.."
input_pdf = f"{PROJ_DIR}/out/voter-cleaned-out.pdf"
output_txt = f"{PROJ_DIR}/out/voter-cleaned.txt"

doc = fitz.open(input_pdf)
page = doc[0]
texts = page.get_text('blocks')

lines = [text[4] for text in texts]
with open(output_txt, 'w', encoding="UTF-8") as fh: fh.writelines(lines)
