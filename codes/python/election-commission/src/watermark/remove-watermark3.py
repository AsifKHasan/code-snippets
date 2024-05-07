#!/usr/bin/env python3

import fitz
# Open the PDF file

input_pdf = '../data/voter-original.pdf'
output_pdf = '../out/voter-wo-watermark.pdf'

pdf = fitz.open(input_pdf)

# Iterate over the pages in the PDF file
for page in pdf:
    # Get the annotations on the page
    annotations = page.annots()
    # Iterate through the annotations
    for annotation in annotations:
        print(f'Annotation on page: {page.number} with type: {annotation.type} and rect: {annotation.rect}')
        # Check if the annotation is a watermark
        if annotation.type[0] == 8:
            # Remove the annotation
            page.deleteAnnot(annotation)
    
# Save the PDF with the watermark removed
pdf.save(output_pdf)