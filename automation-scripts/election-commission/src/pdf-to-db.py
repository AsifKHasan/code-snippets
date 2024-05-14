#!/usr/bin/env python3

''' usage:
    ./pdf-to-db.py --directory ${PROJ_HOME}
    pdf-to-db.py --directory %PROJ_HOME%
    assuming that there is a directory named *data* under this
'''

import os
import re
import argparse
import glob

from helper.logger import *
from pdf.pdf_utils import *


''' dictionary that looks like
    key -> pdf file name
    values ->
        root-dir        : root directory where the pdf is 
        source-dir      : original directory under root where the pdf is 
        cleaned-dir     : directory under root where the cleaned pdf is

        division        : 
            code-from-path      : division code from file path
            name-from-file      : division name from file path

        district        :
            code-from-path      : district code from file path
            name-from-path      : district code from file path
            name-from-file      : district name from file content

        upazila         :
            code-from-path      : upazila code from file path
            name-from-path      : upazila code from file path
            name-from-file      : upazila name from file content

        city-corporation :
            name-from-file      : city corporation/pourasava name from file content

        union           :
            name-from-file      : union name from file content

        ward           :
            number-from-file    : ward number from file content

        voter-area      :
            code-from-path      : voter area code from file path
            code-from-file      : voter area code from file content
            name-from-file      : voter area name from file content

        voter-gender    : 
            from-path       : whether male/female from file name
            from-file       : whether male/female from file content

        voter-count     :
            total-from-file     : total voter count from file content
            gender-from-path    : gender voter count from file name
            gender-from-file    : gender voter count from file content
            gender-from-data    : gender voter count from file data

        voter-data      :
            [
                serial      : 
                number      : 
                name        : 
                father      : 
                husband     : 
                mother      : 
                occupation  :
                dob         :
                address     : 
            ]
'''

ROOT_DIR = None



''' parse path and filename to get some basic info
'''
def parse_data_objects(file_name, data):
    # parse file_name
    parts = file_name.split('_')
    if len(parts) != 8:
        warn(f"{file_name} : should have seven elements separated by _. Found {len(parts)} ... skipping")
        return

    # update data - 930121_com_636_female_without_photo_38_2024-3-21
    data['voter-area']['code-from-path'] = parts[0]
    data['voter-gender']['from-path'] = parts[3]
    data['voter-count']['gender-from-path'] = int(parts[2])

    # prepare page-dir
    data['pages-dir'] = f"{data['source-dir'].replace('/data/', '/out/', 1)}/{data['voter-area']['code-from-path']}-{data['voter-gender']['from-path']}/pages"
    data['segments-dir'] = f"{data['source-dir'].replace('/data/', '/out/', 1)}/{data['voter-area']['code-from-path']}-{data['voter-gender']['from-path']}/segments"
    data['texts-dir'] = f"{data['source-dir'].replace('/data/', '/out/', 1)}/{data['voter-area']['code-from-path']}-{data['voter-gender']['from-path']}/texts"

    # make sure the pages dir exists
    pages_dir = f"{data['root-dir']}/{data['pages-dir']}"
    os.makedirs(pages_dir, exist_ok=True)

    segments_dir = f"{data['root-dir']}/{data['segments-dir']}"
    os.makedirs(segments_dir, exist_ok=True)

    texts_dir = f"{data['root-dir']}/{data['texts-dir']}"
    os.makedirs(texts_dir, exist_ok=True)



''' print header data gathered from path and filename
'''
def print_header(file_name, data):
    info(f"from pdf path", nesting_level=1)
    info(f"{data['page-count']} pages", nesting_level=2)
    info(f"voter area   : {data['voter-area']['code-from-path']}", nesting_level=2)
    info(f"voter gender : {data['voter-gender']['from-path']}", nesting_level=2)
    info(f"voter count  : {data['voter-count']['gender-from-path']}", nesting_level=2)
    print()



''' remove watermark and save pdf pages as individual images
'''
def clean_and_save_pages(file_name, data, no_page_saving=False, dpi=600):
    input_pdf = f"{data['root-dir']}/{data['source-dir']}/{file_name}"
    debug(f"generating page images at [{dpi}] dpi", nesting_level=1)

    # directory where output images will be saved
    output_img_folder = f"{data['root-dir']}/{data['pages-dir']}"
    num_pages = clean_and_pagify(input_pdf=input_pdf, output_img_folder=output_img_folder, no_page_saving=no_page_saving, clean_images=True, watermark_is_image=False, dpi=dpi)
    data['page-count'] = num_pages
    debug(f"[{num_pages}] page images generated at [{dpi}] dpi", nesting_level=1)
    print()



''' parse the first page of the pdf
'''
def parse_top_sheet(file_name, data, dpi=600):
    LINES_EXPECTED = 5

    page_no = 0

    top_sheet_image = f"{data['root-dir']}/{data['pages-dir']}/page-{page_no:03d}.png"

    debug(f"parsing page [{page_no}] at [{dpi}] dpi", nesting_level=1)
    page_texts = page_text_tesseract(image_file=top_sheet_image, dpi=dpi)
    # page_texts = page_text_easyocr(pdf_file=pdf_file, page_num=0)
    # page_texts = page_text_mupdf(image_file=top_sheet_image)
    debug(f"page [{page_no}] parsed at [{dpi}] dpi", nesting_level=1)
    print()

    # print(page_texts)
    
    info(f"from top sheet", nesting_level=1)

    # tesseract output parsing
    # keep only lines of interest
    prefixes = ['উপজেলা/থানা', 'ইউনিয়ন/ পৌর ওয়ার্ড', 'ক্যান্টনমেন্ট বোর্ড', 'ভোটার এলাকা', 'সর্বমোট ভোটার সংখ্যা', 'ভোটার এলাকার নম্বর', 'মোট ', ]
    lines = page_texts.split('\n')
    filtered_lines = [line for line in lines if any(line.startswith(prefix) for prefix in prefixes)]

    if len(filtered_lines) != LINES_EXPECTED:
        error(f"top sheet should have [{LINES_EXPECTED}] lines, but found [{len(filtered_lines)}] lines", nesting_level=2)

    data['top-sheet-lines'] = filtered_lines
    # print('\n'.join(filtered_lines))

    # Upazila and City corporation are in the first line
    # উপজেলা/থানা              দেলদুয়ার                                        সিটি কর্পোরেশন/ পৌরসভা
    text = filtered_lines[0]
    regex = re.compile(r'উপজেলা/থানা\s+?(?P<upazila>.*?)\s+সিটি কর্পোরেশন/ পৌরসভা\s*?(?P<city>.*)', re.MULTILINE)
    m = regex.match(text)
    if m and m.group('upazila'):
        upazila = m.group('upazila').strip()
        debug(f"upazila/thana is [{upazila}]", nesting_level=2)

    else:
        error(f"could not parse upazila/thana name", nesting_level=2)

    if m and m.group('city'):
        city = m.group('city').strip()
        debug(f"city corporation/pourasava is [{city}]", nesting_level=2)

    else:
        warn(f"could not parse city corporation/pourasava name", nesting_level=2)


    # Union is in second line
    # ইউনিয়ন/ পৌর ওয়ার্ড ডুবাইল
    text = filtered_lines[1]
    regex = re.compile(r'ইউনিয়ন/ পৌর ওয়ার্ড.*\s+?(?P<union>.*)', re.MULTILINE)
    m = regex.match(text)
    if m and m.group('union'):
        union = m.group('union').strip()
        debug(f"union/ward is [{union}]", nesting_level=2)

    else:
        error(f"could not parse union/word name", nesting_level=2)


    # Ward number is in third line
    # ওয়ার্ড নম্বর ইউনিয়ন পরিষদের জন্য) ২
    text = filtered_lines[2]
    regex = re.compile(r'.+ওয়ার্ড নম্বর [(]*ইউনিয়ন পরিষদের জন্য[)]*\s+?(?P<ward>.*)', re.MULTILINE)
    m = regex.match(text)
    if m and m.group('ward'):
        ward = m.group('ward').strip()
        debug(f"ward number is [{ward}]", nesting_level=2)

    else:
        error(f"could not parse ward number", nesting_level=2)


    # Voter area and Total Voter Count are in the fourth line
    # ভোটার এলাকা         ইসলামপুর                            সর্বমোট ভোটার সংখ্যা                 ১০২০
    text = filtered_lines[3]
    regex = re.compile(r'ভোটার এলাকা\s+?(?P<voter_area>.*?)\s+সর্বমোট ভোটার সংখ্যা\s*?(?P<total_voters>.*)', re.MULTILINE)
    m = regex.match(text)
    if m and m.group('voter_area'):
        voter_area = m.group('voter_area').strip()
        debug(f"voter area is [{voter_area}]", nesting_level=2)

    else:
        error(f"could not parse voter area name")

    if m and m.group('total_voters'):
        total_voters = m.group('total_voters').strip()
        debug(f"total voters [{total_voters}]", nesting_level=2)

    else:
        error(f"could not parse total voter number", nesting_level=2)


    # Voter area number and Voter Count by gender are in the fifth line
    # ভোটার এলাকার নম্বর ০১৮১                           মোট পুরুষ ভোটার সংখ্যা             ৫০৮
    text = filtered_lines[4]
    regex = re.compile(r'ভোটার এলাকার নম্বর\s+?(?P<voter_area_number>.*?)\s+মোট (?P<voter_gender>.*?) ভোটার সংখ্যা\s*?(?P<gender_voters>.*)', re.MULTILINE)
    m = regex.match(text)
    if m and m.group('voter_area_number'):
        voter_area_number = m.group('voter_area_number').strip()
        debug(f"voter area number is [{voter_area_number}]", nesting_level=2)

    else:
        error(f"could not parse voter area number", nesting_level=2)

    if m and m.group('voter_gender'):
        voter_gender = m.group('voter_gender').strip()
        debug(f"voter gender is [{voter_gender}]", nesting_level=2)

    else:
        voter_gender = 'UNKNOWN'
        error(f"could not parse voter gender", nesting_level=2)

    if m and m.group('gender_voters'):
        gender_voters = m.group('gender_voters').strip()
        debug(f"total {voter_gender} voters [{gender_voters}]", nesting_level=2)

    else:
        error(f"could not parse {voter_gender} voter number", nesting_level=2)

    print()



''' segment pages for text blocks
'''
def segment_pages(file_name, data, no_segmentation=False, page_list=None, dpi=600):
    if no_segmentation:
        return

    for page_no in range(2, data['page-count']):
        if page_list and page_no in page_list:
            page_image_name = f"page-{page_no:03d}"
            page_image_path = f"{data['root-dir']}/{data['pages-dir']}/{page_image_name}.png"
            segment_output_directory = f"{data['root-dir']}/{data['segments-dir']}/{page_image_name}"
            os.makedirs(segment_output_directory, exist_ok=True)

            info(f"segmenting [{page_image_name}.png]", nesting_level=1)
            image_segments = segment_image(page_image_path=page_image_path, no_segmentation=False)
            info(f"[{len(image_segments)}] segments found", nesting_level=2)

            segments_saved = save_image_segments(image_segments=image_segments, page_image_name=page_image_name, segment_output_directory=segment_output_directory, segment_min_height=500, dpi=dpi)
            info(f"[{segments_saved}] segments saved at [{dpi}] dpi", nesting_level=2)

            print()

    print()



''' parse segments through OCR
'''
def parse_segments(file_name, data, page_list=None, dpi=600):
    num_lines_in_segment = 6
    for page_no in range(2, data['page-count']):
        if page_list and page_no in page_list:
            page_image_name = f"page-{page_no:03d}"
            image_segments_path = f"{data['root-dir']}/{data['segments-dir']}/{page_image_name}"

            if not os.path.exists(image_segments_path):
                warn(f"segments directory for [{page_image_name}] : [{image_segments_path}] does not exist", nesting_level=2)
                continue

            text_output_directory = f"{data['root-dir']}/{data['texts-dir']}/{page_image_name}"
            os.makedirs(text_output_directory, exist_ok=True)


            # traverse segments-dir for .png files
            info(f"parsing segments for [{page_image_name}]", nesting_level=2)
            segment_files = glob.glob('*.png', root_dir=image_segments_path)
            segment_count = 0
            for segment_file in segment_files:
                segment_count = segment_count + 1
                segment_path = f"{image_segments_path}/{segment_file}"
                text_output_path = f"{text_output_directory}/{segment_file.replace('.png', '.txt')}"

                info(f"parsing segment [{segment_file}]", nesting_level=3)
                text = page_text_tesseract(image_file=segment_path, dpi=dpi)

                # process text
                text = text.strip()
                text = text.replace('\n\n', '\n')
                if text != "":
                    with open(text_output_path, 'w', encoding='UTF-8') as fh:
                        fh.write(text)

                # validate text
                text_lines = text.split('\n')
                if len(text_lines) != num_lines_in_segment:
                    error(f"expected [{num_lines_in_segment}] lines, found [{len(text_lines)}]", nesting_level=4)
                else:
                    debug(f"found [{len(text_lines)}] lines", nesting_level=4)


                info(f"parsing segment [{segment_file}] .. DONE", nesting_level=3)
                print()
 
            info(f"[{segment_count}] segment(s) parsed for [{page_image_name}]", nesting_level=2)

            print()

    print()



''' traverse input directory for (pdf) files and collect information in a dictionary for each file
'''
def traverse_directory(root_path, path_patterns=[]):
    DATA = {}
    count = 0
    for root, dirs, files in os.walk(root_path):
        path = root.replace(ROOT_DIR, '')

        for file in files:
            file_path = f"{path}/{file}"
            if file.endswith('.pdf'):
                # check if the path falls under any of the patterns
                matches = False
                if len(path_patterns) == 0:
                    matches = True
                
                else:
                    for pattern in path_patterns:
                        # print(file_path)
                        result = re.match(pattern, file_path)
                        if result:
                            matches = True
                            break

                if matches:
                    DATA[file] = {'root-dir': ROOT_DIR, 'source-dir': path.replace('\\', '/'), 'division': {}, 'district': {}, 'upazila': {}, 'city-corporation': {}, 'union': {}, 'ward': {}, 'voter-area': {}, 'voter-gender': {}, 'voter-count': {}, 'voter-data': []}
                    count = count + 1

            else:
                warn(f"{file} is not a pdf ... skipping")

    return DATA



if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--directory", required=True, help="directory where the pdfs are", default=argparse.SUPPRESS)
	args = vars(ap.parse_args())

    # there must be a *data* directory under ROOT_DIR
	ROOT_DIR = args['directory'].replace('\\', '/')
	# path_patterns = [r".*930119_.+_female.*"]
	path_patterns = [r".*930119.*"]
	DATA = traverse_directory(root_path=f"{ROOT_DIR}/data", path_patterns=path_patterns)
	info(ROOT_DIR, nesting_level=0)
	for file_name, data in DATA.items():
		info(f"{file_name}", nesting_level=0)

		parse_data_objects(file_name=file_name, data=data)
		no_page_saving = False
		clean_and_save_pages(file_name=file_name, data=data, no_page_saving=no_page_saving, dpi=600)
		print_header(file_name=file_name, data=data)
		parse_top_sheet(file_name=file_name, data=data, dpi=400)
		page_list = [2]
		no_segmentation = False
		segment_pages(file_name=file_name, data=data, no_segmentation=no_segmentation, page_list=page_list, dpi=600)
		parse_segments(file_name=file_name, data=data, page_list=page_list, dpi=600)
        
		info(f"{file_name} .. DONE", nesting_level=0)
		print()
