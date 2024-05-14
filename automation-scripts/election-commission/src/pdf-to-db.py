#!/usr/bin/env python3

''' usage:
    ./pdf-to-db.py --directory ${PROJ_HOME}
    pdf-to-db.py --directory %PROJ_HOME%
    assuming that there is a directory named *data* under this
'''

import os
import re
import argparse

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
DATA = {}



''' parse path and filename to get some basic info
'''
def parse_data_objects():
    for file_name, data in DATA.items():
        # parse file_name
        parts = file_name.split('_')
        if len(parts) != 8:
            warn(f"{file_name} : should have seven elements separated by _. Found {len(parts)} ... skipping")
            continue

        # update data - 930121_com_636_female_without_photo_38_2024-3-21
        data['voter-area']['code-from-path'] = parts[0]
        data['voter-gender']['from-path'] = parts[3]
        data['voter-count']['gender-from-path'] = int(parts[2])

        # prepare page-dir
        data['pages-dir'] = f"{data['source-dir'].replace('/data/', '/out/pages/', 1)}/{data['voter-area']['code-from-path']}-{data['voter-gender']['from-path']}"

        # make sure the pages dir exists
        pages_dir = f"{data['root-dir']}/{data['pages-dir']}"
        os.makedirs(pages_dir, exist_ok=True)



''' print data gathered
'''
def print_data():
    print(ROOT_DIR)
    for file_name, data in DATA.items():
        info(data['source-dir'])
        info(f".. {file_name}")
        # info(f".. {data['pages']} pages")
        info(f".... voter area   : {data['voter-area']['code-from-path']}")
        info(f".... voter gender : {data['voter-gender']['from-path']}")
        info(f".... voter count  : {data['voter-count']['gender-from-path']}")
        info(f".... cleaned path : {data['cleaned-dir']}")
        print()



''' remove watermark and save pdf pages as individual images
'''
def clean_and_save_pdfs():
    for file_name, data in DATA.items():
        input_pdf = f"{data['root-dir']}/{data['source-dir']}/{file_name}"
        debug(f"processing source [{data['source-dir']}/{file_name}]")

        # directory where output images will be saved
        output_img_folder = f"{data['root-dir']}/{data['pages-dir']}"
        num_pages = clean_pdf(input_pdf=input_pdf, output_img_folder=output_img_folder, clean_images=True, watermark_is_image=False, dpi=600)
        data['pages'] = num_pages



''' parse the first page of the pdf
'''
def parse_top_sheet():
    for file_name, data in DATA.items():
        page_no = 0
        top_sheet_image = f"{data['root-dir']}/{data['pages-dir']}/page-{page_no:03d}.png"
        pdf_file = f"{data['root-dir']}/{data['cleaned-dir']}/{file_name}"
        page_texts = page_text_tesseract(image_file=top_sheet_image)
        # page_texts = page_text_easyocr(pdf_file=pdf_file, page_num=0)
        # page_texts = page_text_mupdf(pdf_file=pdf_file, page_num=0)

        print(page_texts)
        
        # tesseract output parsing
        # keep only lines of interest
        prefixes = ['উপজেলা/থানা', 'ইউনিয়ন/ পৌর ওয়ার্ড', 'ওয়ার্ড নম্বর', 'ভোটার এলাকা', 'সর্বমোট ভোটার সংখ্যা', 'ভোটার এলাকার নম্বর', 'মোট ', ]
        lines = page_texts.split('\n')
        filtered_lines = [line for line in lines if any(line.startswith(prefix) for prefix in prefixes)]

        if len(filtered_lines) != 5:
            error(f"top sheet should have [5] lines, but found [{len(filtered_lines)}] lines")

        # text = '\n'.join(filtered_lines)

        # Upazila and City corporation are in the first line
        # উপজেলা/থানা              দেলদুয়ার                                        সিটি কর্পোরেশন/ পৌরসভা
        text = filtered_lines[0]
        regex = re.compile(r'উপজেলা/থানা\s+?(?P<upazila>.*?)\s+সিটি কর্পোরেশন/ পৌরসভা\s*?(?P<city>.*)', re.MULTILINE)
        m = regex.match(text)
        if m and m.group('upazila'):
            upazila = m.group('upazila').strip()
            debug(f"upazila/thana is [{upazila}]")

        else:
            error(f"could not parse upazila/thana name")

        if m and m.group('city'):
            city = m.group('city').strip()
            debug(f"city corporation/pourasava is [{city}]")

        else:
            error(f"could not parse city corporation/pourasava name")


        # Union is in second line
        # ইউনিয়ন/ পৌর ওয়ার্ড ডুবাইল
        text = filtered_lines[1]
        regex = re.compile(r'ইউনিয়ন/ পৌর ওয়ার্ড\s+?(?P<union>.*)', re.MULTILINE)
        m = regex.match(text)
        if m and m.group('union'):
            union = m.group('union').strip()
            debug(f"union/ward is [{union}]")

        else:
            error(f"could not parse union/word name")


        # Ward number is in third line
        # ওয়ার্ড নম্বর ইউনিয়ন পরিষদের জন্য) ২
        text = filtered_lines[2]
        regex = re.compile(r'ওয়ার্ড নম্বর [(]*ইউনিয়ন পরিষদের জন্য[)]*\s+?(?P<ward>.*)', re.MULTILINE)
        m = regex.match(text)
        if m and m.group('ward'):
            ward = m.group('ward').strip()
            debug(f"ward number is [{ward}]")

        else:
            error(f"could not parse ward number")


        # Voter area and Total Voter Count are in the fourth line
        # ভোটার এলাকা         ইসলামপুর                            সর্বমোট ভোটার সংখ্যা                 ১০২০
        text = filtered_lines[3]
        regex = re.compile(r'ভোটার এলাকা\s+?(?P<voter_area>.*?)\s+সর্বমোট ভোটার সংখ্যা\s*?(?P<total_voters>.*)', re.MULTILINE)
        m = regex.match(text)
        if m and m.group('voter_area'):
            voter_area = m.group('voter_area').strip()
            debug(f"voter area is [{voter_area}]")

        else:
            error(f"could not parse voter area name")

        if m and m.group('total_voters'):
            total_voters = m.group('total_voters').strip()
            debug(f"total voters [{total_voters}]")

        else:
            error(f"could not parse total voter number")


        # Voter area number and Voter Count by gender are in the fifth line
        # ভোটার এলাকার নম্বর ০১৮১                           মোট পুরুষ ভোটার সংখ্যা             ৫০৮
        text = filtered_lines[4]
        regex = re.compile(r'ভোটার এলাকার নম্বর\s+?(?P<voter_area_number>.*?)\s+মোট (?P<voter_gender>.*?) ভোটার সংখ্যা\s*?(?P<gender_voters>.*)', re.MULTILINE)
        m = regex.match(text)
        if m and m.group('voter_area_number'):
            voter_area_number = m.group('voter_area_number').strip()
            debug(f"voter area number is [{voter_area_number}]")

        else:
            error(f"could not parse voter area number")

        if m and m.group('voter_gender'):
            voter_gender = m.group('voter_gender').strip()
            debug(f"voter gender is [{voter_gender}]")

        else:
            voter_gender = 'UNKNOWN'
            error(f"could not parse voter gender")

        if m and m.group('gender_voters'):
            gender_voters = m.group('gender_voters').strip()
            debug(f"total {voter_gender} voters [{gender_voters}]")

        else:
            error(f"could not parse {voter_gender} voter number")


        # get gender - ভোটার তালিকা - (মহিলা)



''' traverse input directory for (pdf) files and collect information in a dictionary for each file
'''
def traverse_directory(root_path, limit=0):
    count = 0
    for root, dirs, files in os.walk(root_path):
        path = root.replace(ROOT_DIR, '')

        for file in files:
            if file.endswith('.pdf'):
                DATA[file] = {'root-dir': ROOT_DIR, 'source-dir': path.replace('\\', '/'), 'cleaned-dir': None, 'division': {}, 'district': {}, 'upazila': {}, 'city-corporation': {}, 'union': {}, 'ward': {}, 'voter-area': {}, 'voter-gender': {}, 'voter-count': {}, 'voter-data': []}
                count = count + 1
                if limit and count >= limit:
                    return

            else:
                warn(f"{file} is not a pdf ... skipping")



if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--directory", required=True, help="directory where the pdfs are", default=argparse.SUPPRESS)
	args = vars(ap.parse_args())

    # there must be a *data* directory under ROOT_DIR
	ROOT_DIR = args['directory'].replace('\\', '/')
	traverse_directory(root_path=f"{ROOT_DIR}/data", limit=1)
	parse_data_objects()
	clean_and_save_pdfs()
	parse_top_sheet()
	print_data()
