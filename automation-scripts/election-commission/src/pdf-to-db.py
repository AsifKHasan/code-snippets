#!/usr/bin/env python3

''' usage:
    ./pdf-to-db.py --directory ${PROJ_HOME} assuming that there is a directory named *data* under this
'''

import os
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



'''
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

        # prepare cleaned-dir
        data['cleaned-dir'] = data['source-dir'].replace('/data/', '/out/cleaned/', 1)

        # make sure the cleaned dir exists
        cleaned_dir = f"{data['root-dir']}/{data['cleaned-dir']}"
        os.makedirs(cleaned_dir, exist_ok=True)



'''
'''
def print_data():
    print(ROOT_DIR)
    for file_name, data in DATA.items():
        info(data['source-dir'])
        info(f".. {file_name}")
        info(f".... voter area   : {data['voter-area']['code-from-path']}")
        info(f".... voter gender : {data['voter-gender']['from-path']}")
        info(f".... voter count  : {data['voter-count']['gender-from-path']}")
        info(f".... cleaned path : {data['cleaned-dir']}")
        print()



'''
'''
def clean_and_save_pdfs():
    for file_name, data in DATA.items():
        input_pdf = f"{data['root-dir']}/{data['source-dir']}/{file_name}"
        output_pdf = f"{data['root-dir']}/{data['cleaned-dir']}/{file_name}"
        clean_pdf(input_pdf=input_pdf, output_pdf=output_pdf)



''' traverse input directory for (pdf) files and collect information in a dictionary for each file
'''
def traverse_directory(root_path):
    for root, dirs, files in os.walk(root_path):
        path = root.replace(ROOT_DIR, '')
        for file in files:
            if file.endswith('.pdf'):
                DATA[file] = {'root-dir': ROOT_DIR, 'source-dir': path, 'cleaned-dir': None, 'division': {}, 'district': {}, 'upazila': {}, 'city-corporation': {}, 'union': {}, 'ward': {}, 'voter-area': {}, 'voter-gender': {}, 'voter-count': {}, 'voter-data': []}
            else:
                warn(f"{file} is not a pdf ... skipping")



if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--directory", required=True, help="directory where the pdfs are", default=argparse.SUPPRESS)
	args = vars(ap.parse_args())

    # there must be a *data* directory under ROOT_DIR
	ROOT_DIR = args['directory']
	traverse_directory(root_path=f"{ROOT_DIR}/data")
	parse_data_objects()
	clean_and_save_pdfs()
	print_data()
