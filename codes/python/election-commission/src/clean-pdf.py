#!/usr/bin/env python3

import fitz

PROJ_DIR = '..'
input_pdf = f"{PROJ_DIR}/data/voter-original.pdf"
output_pdf = f"{PROJ_DIR}/out/voter-cleaned.pdf"

def img_replace(page, xref, filename=None, stream=None, pixmap=None):
    """Replace image identified by xref.

    Args:
        page: a fitz.Page object
        xref: cross reference number of image to replace
        filename, stream, pixmap: must be given as for
        page.insert_image().

    """
    if bool(filename) + bool(stream) + bool(pixmap) != 1:
        raise ValueError("Exactly one of filename/stream/pixmap must be given")
    doc = page.parent  # the owning document
    # insert new image anywhere in page
    new_xref = page.insert_image(
        page.rect, filename=filename, stream=stream, pixmap=pixmap
    )
    doc.xref_copy(new_xref, xref)  # copy over new to old
    last_contents_xref = page.get_contents()[-1]
    # new image insertion has created a new /Contents source,
    # which we will set to spaces now
    doc.update_stream(last_contents_xref, b" ")


if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 5):
    raise ValueError("Need v1.19.5+")

# open input
doc = fitz.open(input_pdf)

# remove all images in all pages
for page in doc:
    images = page.get_images()  
    for item in images:
        item = images[0]
        old_xref = item[0]

        pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 1, 1), 1)
        pix.clear_with()
        img_replace(page, old_xref, pixmap=pix)

# remove first two pages
l = list(range(2, doc.page_count))
doc.select(l)

# save output
doc.ez_save(output_pdf, garbage=4)
