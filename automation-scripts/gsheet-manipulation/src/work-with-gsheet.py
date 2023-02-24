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

WORKSHEET_NAMES = [
<<<<<<< HEAD
    '01-DP-1-ITT',
    'A-annex',
    'A-DP-2-schedule',
    'B-annex',
    'B-DP-3-cover-letter',
    'C-annex',
    'C-DP-4-special-terms',
    'D-annex',
    'D-technical-spec',
    'E-annex',
    'E0-remarks-column-10',
    'E1-appendix-QAC',
    'F-annex',
    'F-terms-conditions',
    'G-annex',
    'G0-remarks-column-11',
    'G1-appendix-QAC',
    'H-annex',
    'H-terms-clauses',
    'J-annex',
    'J-training-req',
    'K-annex',
    'K0-req-analyzer',
    'K1-appendix-finding-list',
    'K2-appendix-service-tools',
    'K3-appendix-spare-parts',
    'L-annex',
    'L-DP-6-financial-offer',
    'M-annex',
    'M-DP-7-performance-guarantee',
    'N-annex',
    'N-DP-8-EUC',
    'P-annex',
    'P-DP-9-terms-local-currency',
    'Q-annex',
    'Q-undertaking'
=======
    '03-system-features-requirements',
    '03.01-functional-requirements',
    '03.02-external-interface-requirements',
    '03.03-system-features',
    '03.04-nonfunctional-requirements',
    '03.04.01-security-requirements',
    '03.04.02-usability-requirements',
    '03.04.03-scalability-requirements',
    '03.04.04-performance-requirements',
>>>>>>> d1a6f382992f8799da8b1839e5a97f97e97d73c5
]

RANGE_WORK_SPECS = {
    'B4': {'value': '10004 (02493)', 'valign': 'center'}, 
    'C4': {'value': '10004 (02493)', 'valign': 'center'}, 
    'D4': {'value': '10004 (02493)', 'valign': 'center'}, 
    'E4': {'value': '10004 (02493)', 'valign': 'center'}, 
    'F4': {'value': '10004 (02493)', 'valign': 'center'}, 
    'G4': {'value': '10004 (02493)', 'valign': 'center'}, 

    'B5': {'value': '10004 (02493)', 'valign': 'center'}, 
    'C5': {'value': '10004 (02493)', 'valign': 'center'}, 
    'D5': {'value': '10004 (02493)', 'valign': 'center'}, 
    'E5': {'value': '10004 (02493)', 'valign': 'center'}, 
    'F5': {'value': '10004 (02493)', 'valign': 'center'}, 
    'G5': {'value': '10004 (02493)', 'valign': 'center'}, 
}

def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related

    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')
    
    # END   drive file related
    pass


def work_on_gsheet(g_sheet):

    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=WORKSHEET_NAMES)
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F')
    g_sheet.order_worksheets()

    # g_sheet.remove_worksheet(worksheet_name='-toc')

    # g_sheet.rename_worksheet(worksheet_name='summary', new_worksheet_name='01-summary')

    # g_sheet.work_on_ranges(worksheet_name='11-result', range_work_specs=RANGE_WORK_SPECS)
    # g_sheet.remove_trailing_blank_rows(worksheet_name='-toc-new')

    # for worksheet_name in WORKSHEET_NAMES:
    #     num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name)
    #     print(f"{g_sheet.title:<30}: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")


    # BEGIN common tasks
    # new_toc_from_toc(g_sheet)
    # create_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # format_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # END   common tasks


    # BEGIN adhoc tasks
    # populate_range(g_sheet=g_sheet)
    # insert_a_row_with_values(g_sheet=g_sheet)
    # create_review_notes_conditional_formatting(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # END   adhoc tasks


    # BEGIN resume specific tasks
    # create_06_job_history_new(g_sheet)
    # END   resume specific tasks


    # BEGIN Tanim ACAS tasks
    # RANGE_WORK_SPECS = get_ranked_result()
    # g_sheet.work_on_ranges(worksheet_name='11-result', range_work_specs=RANGE_WORK_SPECS)
    # END   Tanim ACAS tasks


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
        if count % 50 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)