#!/usr/bin/env python3

import fitz
# Solution 2
# Open the PDF file
pdf = fitz.open('C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-original.pdf')

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
pdf.save('C:/Users/Asif Hasan/Downloads/personal/voter-list/voter-wo-watermark.pdf')