#!/usr/bin/env python3

import io
import fitz
# import pprint
# import easyocr
import pytesseract
import ocrmypdf
from PIL import Image
# from pypdf import PdfReader, PdfWriter
# from pypdf.generic import ContentStream, NameObject, TextStringObject
from pdf2image import convert_from_path

mat = fitz.Matrix(2, 2)  # high resolution matrix

def ocr_the_page(page):
    """Extract the text from passed-in PDF page."""
    src = page.parent  # the page's document
    doc = fitz.open()  # make temporary 1-pager
    doc.insert_pdf(src, from_page=page.number, to_page=page.number)
    pdfbytes = doc.tobytes()
    inbytes = io.BytesIO(pdfbytes)  # transform to BytesIO object
    outbytes = io.BytesIO()  # let ocrmypdf store its result pdf here
    ocrmypdf.ocr(
        inbytes,  # input 1-pager
        outbytes,  # ouput 1-pager
        # image_dpi=600,
        language="ben",  # modify as required e.g. ("eng", "ger")
        output_type="pdf",  # only need simple PDF format
        # add more paramneters, e.g. to enforce OCR-ing, etc., e.g.
        force_ocr=True,
        clean=True,
        # remove_background=True,
        progress_bar=False,
        # oversample=600,
    )
    ocr_pdf = fitz.open("pdf", outbytes.getvalue())  # read output as fitz PDF
    text = ocr_pdf[0].get_text()  # ...and extract text from the page
    return text  # return it

'''
'''
def page_text_tesseract(pdf_file, page_num):
    config = '-c preserve_interword_spaces=1 --psm 4 --oem 3'

    pages = convert_from_path(pdf_file, dpi=600, first_page=page_num, last_page=page_num+1)
    for page_no, img in enumerate(pages):
        text = pytesseract.image_to_string(img, lang='ben', config=config)

    return text



def page_text_easyocr(pdf_file, page_num):
    global mat
    easyocr_reader = easyocr.Reader(['bn'])

    # open input
    doc = fitz.open(pdf_file)

    page = doc[page_num]
    pix = page.get_pixmap(colorspace=fitz.csGRAY, matrix=mat)
    img = pix.tobytes("png")

    texts = easyocr_reader.readtext(img, detail=0, paragraph=True)
    text = '\n'.join(texts)

    return text



def page_text_mupdf(pdf_file, page_num):
    # open input
    doc = fitz.open(pdf_file)

    page = doc[page_num]
    # texts = page.get_text('html')
    text_page = page.get_textpage_ocr(flags=3, language='ben', dpi=600, full=True)
    texts = text_page.extractText(sort=True)

    # texts = ocr_the_page(page)
    
    return texts
            


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
    
    # open input
    doc = fitz.open(input_pdf)

    if watermark_is_image:
        wm_text = b'\x00/\x00O\x00Y\x00K\x01"\x00\x03\x00\xcf\x00A\x00K\x004\x00K\x00D\x00\x03\x009\x00K\x00L\x00E\x00*\x00K'
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
        wm_text = b'002f004f0059004b0122000300cf0041004b0034004b004400030039004b004c0045002a004b'
        replace_with = b''

        # remove text
        for page in doc:
            for xref in page.get_contents():
                stream = doc.xref_stream(xref)
                stream = stream.replace(wm_text, replace_with)
                doc.update_stream(xref, stream)

        # remove second page
        l = [0] + list(range(2, doc.page_count))
        doc.select(l)

        # save output
        doc.ez_save(output_pdf, garbage=4)

    # else:
    #     reader = PdfReader(input_pdf)
    #     writer = PdfWriter()

    #     l = [0] + list(range(2, len(reader.pages)))
    #     for p in l:
    #         page = reader.pages[p]

    #         # Get the current page's contents
    #         content_object = page["/Contents"]
    #         content = ContentStream(content_object, reader)

    #         # Loop over all pdf elements
    #         for operands, operator in content.operations:
    #             # Was told to adapt this part dependent on my PDF file
    #             if operator == b"Tj":
    #                 if len(operands) and operands[0] == wm_text:
    #                     operands[0] = TextStringObject("")

    #         # Set the modified content as content object on the page
    #         page.__setitem__(NameObject("/Contents"), content)

    #         # Add the page to the output
    #         writer.add_page(page)

    #     # Write the stream
    #     with open(output_pdf, 'wb') as fh:
    #         writer.write(fh)

