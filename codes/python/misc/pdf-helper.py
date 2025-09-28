import PyPDF2

input_files = [

    "LGRD-UPEHSDP__GA__12__software-technical-solution-design-and-integration-subplan.pdf",
]

watermark_file = "./original.pdf"
watermark_file = "./copy1.pdf"
watermark_file = "./copy2.pdf"

for input_file in input_files:
    output_file = "./topsheets/original__" + input_file
    output_file = "./topsheets/copy1__" + input_file
    output_file = "./topsheets/copy2__" + input_file

    with open("./GA/" + input_file, "rb") as filehandle_input:
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            # get first page of the original PDF
            first_page = pdf.getPage(0)

            # get first page of the watermark PDF
            first_page_watermark = watermark.getPage(0)

            # merge the two pages
            first_page.mergePage(first_page_watermark)

            # create a pdf writer object for the output file
            pdf_writer = PyPDF2.PdfFileWriter()

            # add page
            pdf_writer.addPage(first_page)

            with open(output_file, "wb") as filehandle_output:
                # write the watermarked file to the new file
                pdf_writer.write(filehandle_output)
