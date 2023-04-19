#!/usr/bin/env python3

import json
import yaml
import time
import argparse

# from google.google_sheet import GoogleSheet
from ggle.google_service import GoogleService

from helper.logger import *

from task.common_tasks import *
# from task.resume_tasks import *
# from task.acas_tasks import *

# list of gsheets which are targets for work like copy_to
DESTINATION_GSHEETS = [
]

# list of worksheets on which to do a common work
WORKSHEET_NAMES = [
    '00-layout',
    '00-layout-USAID-FFBT',
    '00-layout-NBR-BSW',
    '01-personal',
    '02-career-highlight',
    '03-education',
    '04-managerial-expertise',
    '05-technical-expertise',
    '06-job-history',
    '07-project-roles',
    '08-training',
    '09-certification',
    '10-membership',
    '11-language-proficiency',
    '12-contact',
    '13-educational-certificates',
    '14-vendor-certificates',
    '15-institutional-certificates',
    '16-references',
    'z-footer',
    'z-header',
]

# work specs for applying on a list of worksheets
RANGE_WORK_SPECS = {
    # change fonts and vertical alignments for worksheet
    'A1:I' : {'font-family': 'Arial', 'font-size': 10, 'valign': 'top'},
    # link -toc-new at cell A1
    'A1' : {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'weight': 'normal', 'halign': 'left'},

}

def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related

    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')

    # END   drive file related
    pass


def work_on_gsheet(g_sheet, g_service):

    # worksheet duplication
    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=WORKSHEET_NAMES)


    # worksheet removal
    # for ws_name in WORKSHEET_NAMES:
        # g_sheet.remove_worksheet(worksheet_name=ws_name)


    # worksheet renaming
    # g_sheet.rename_worksheet(worksheet_name='06-job-history-ffbt', new_worksheet_name='06-job-history-USAID-FFBT')


    # worksheet creation, formatting and related tasks
    # create_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # format_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # create_review_notes_conditional_formatting(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)


    # work on ranges and etc.
    # g_sheet.work_on_ranges(worksheet_names=WORKSHEET_NAMES, range_work_specs=RANGE_WORK_SPECS)
    # for worksheet_name in WORKSHEET_NAMES:
        # g_sheet.remove_trailing_blank_rows(worksheet_name='-toc-new')
        # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name)
        # print(f"{g_sheet.title:<30}: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")
        # pass


    # cell linking and ordering
    # g_sheet.link_cells_to_drive_files(worksheet_name='-toc-new', range_spec_for_cells_to_link='F8:F14')
    # g_sheet.link_cells_to_drive_files(worksheet_name='-toc-new', range_spec_for_cells_to_link='F24:F26')

    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F21')
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F28:F28')
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F41:F')

    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='O4:O')
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='R4:R')
    # g_sheet.order_worksheets()


    # copy worksheets to another gsheet
    # destination_gsheet = g_service.open(DESTINATION_GSHEETS[0])
    # if destination_gsheet:
    #     for worksheet_name in WORKSHEET_NAMES:
            # g_sheet.copy_worksheet_to_gsheet(destination_gsheet, worksheet_name_to_copy=worksheet_name)
            # pass


    # BEGIN common tasks
    # new_toc_from_toc(g_sheet)
    # END   common tasks


    # BEGIN adhoc tasks
    # populate_range(g_sheet=g_sheet)
    # insert_a_row_with_values(g_sheet=g_sheet)
    # END   adhoc tasks


    # BEGIN resume specific tasks
    # create_06_job_history_new(g_sheet)
    # END   resume specific tasks


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
            work_on_gsheet(g_sheet=g_sheet, g_service=g_service)
            # work_on_drive(g_service=g_service, g_sheet=g_sheet)
            info(f"processed  {count:>4}/{num_gsheets} gsheet {gsheet_name}\n")

        wait_for = 60
        if count % 60 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)
