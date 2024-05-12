#!/usr/bin/env python3

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, TextStringObject

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



''' clear watermark and delete specific pages
'''
def clean_pdf(input_pdf, output_pdf, watermark_is_image=True):
    wm_text = b'\x00/\x00O\x00Y\x00K\x01"\x00\x03\x00\xcf\x00A\x00K\x004\x00K\x00D\x00\x03\x009\x00K\x00L\x00E\x00*\x00K'
    
    # open input
    doc = fitz.open(input_pdf)

    if watermark_is_image:
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
        l = [0] + list(range(2, doc.page_count))
        doc.select(l)

        # save output
        doc.ez_save(output_pdf, garbage=4)

    else:
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
                # Was told to adapt this part dependent on my PDF file
                if operator == b"Tj":
                    if len(operands) and operands[0] == wm_text:
                        operands[0] = TextStringObject("")

            # Set the modified content as content object on the page
            page.__setitem__(NameObject("/Contents"), content)

            # Add the page to the output
            writer.add_page(page)

        # Write the stream
        with open(output_pdf, 'wb') as fh:
            writer.write(fh)

