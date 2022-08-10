#!/usr/bin/env python3

import json
import yaml
import time
import argparse

# from google.google_sheet import GoogleSheet
from ggle.google_service import GoogleService

from task.resume_tasks import *

from helper.logger import *


RANGE_WORK_SPECS = {
    'O3': {'value': 'z-header', 'ws-name-to-link': 'z-header'}, 
    'O4': {'value': 'z-header', 'ws-name-to-link': 'z-header'}, 
    'O5': {'value': 'z-header', 'ws-name-to-link': 'z-header'}, 
    'O6': {'value': 'z-header', 'ws-name-to-link': 'z-header'}, 
    'O7': {'value': 'z-header', 'ws-name-to-link': 'z-header'}, 
    'R3': {'value': 'z-footer', 'ws-name-to-link': 'z-footer'}, 
    'R4': {'value': 'z-footer', 'ws-name-to-link': 'z-footer'}, 
    'R5': {'value': 'z-footer', 'ws-name-to-link': 'z-footer'}, 
    'R6': {'value': 'z-footer', 'ws-name-to-link': 'z-footer'}, 
    'R7': {'value': 'z-footer', 'ws-name-to-link': 'z-footer'}, 
}

def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related
    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')
    
    # END   drive file related
    pass


def work_on_gsheet(g_sheet):

    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='summary', new_worksheet_names=['00-layout'])
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F')

    # g_sheet.rename_worksheet(worksheet_name='00-layout', new_worksheet_name='00-layout-Z')

    # g_sheet.remove_worksheet(worksheet_name='-toc')

    # g_sheet.order_worksheets()

    # g_sheet.work_on_ranges(worksheet_name='-toc-new', range_work_specs=RANGE_WORK_SPECS)

    # g_sheet.remove_trailing_blank_rows(worksheet_name='-toc-new')


    # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name='00-layout')
    # print(f"{g_sheet.title:<30}: [00-layout] : {num_rows} rows, {num_cols} columns")


    # BEGIN major tasks
    # new_toc_from_toc(g_sheet)
    # create_worksheets(g_sheet=g_sheet, worksheet_name_list=['00-layout'])
    format_worksheets(g_sheet=g_sheet, worksheet_name_list=['00-layout'])
    # retouch_worksheets(g_sheet, worksheet_name_list=[])
    # create_06_job_history_new(g_sheet)
    # END   major tasks

    # BEGIN drive/file related
    # g_sheet.share(email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # END   drive/file related

    pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with", default=argparse.SUPPRESS)
    args = vars(ap.parse_args())

    if 'gsheet' in args and args["gsheet"] != '':
        gsheet_names = [args["gsheet"]]
    else:
        # read config.yml to get the list of gsheets
        config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
        gsheet_names = config['gsheets']

    g_service = GoogleService('../conf/credential.json')
    count = 0
    num_gsheets = len(gsheet_names)
    for gsheet_name in gsheet_names:
        count = count + 1
        try:
            info(f"processing {count:>4}/{num_gsheets} gsheet {gsheet_name}")
            g_sheet = g_service.open(gsheet_name=gsheet_name)
        except Exception as e:
            g_sheet = None
            warn(str(e))
            # raise e

        if g_sheet:
            work_on_gsheet(g_sheet=g_sheet)
            # work_on_drive(g_service=g_service, g_sheet=g_sheet)
            info(f"processed  {count:>4}/{num_gsheets} gsheet {gsheet_name}\n")

        wait_for = 60
        if count % 25 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)