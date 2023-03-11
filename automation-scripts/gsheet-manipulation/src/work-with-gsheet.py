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
    '03.01.01.01-administration', 
    '03.01.01.01.01-manage-user', 
    '03.01.01.01.02-manage-user-role', 
    '03.01.01.01.03-manage-profile', 
    '03.01.01.01.04-manage-notification', 
    '03.01.01.01.05-managing-data', 
    '03.01.01.02-configs', 
    '03.01.01.02.01-general-config', 
    '03.01.01.02.02-auto-id-config', 
    '03.01.01.02.03-branch-config', 
    '03.01.01.02.04-samity-config', 
    '03.01.01.02.05-member-config', 
    '03.01.01.02.06-address-config', 
    '03.01.01.02.07-workdays-config', 
    '03.01.01.02.08-holidays-config', 
    '03.01.01.02.09-areas', 
    '03.01.01.02.010-zone', 
    '03.01.01.02.011-region', 
    '03.01.01.02.012-funding-organizations', 
    '03.01.01.02.013-member-samity-transfer-config', 
    '03.01.01.02.014-collection-sheet-config', 
    '03.01.01.02.015-loan-product-category', 
    '03.01.01.02.016-economic-purpose-code', 
    '03.01.01.02.017-economic-purpose', 
    '03.01.01.02.018-dashboard-settings', 
    '03.01.01.03-employees', 
    '03.01.01.03.01-employees-departments', 
    '03.01.01.03.02-employees-designations', 
    '03.01.01.03.03-employees', 
    '03.01.01.03.04-employees-responsibility', 
    '03.01.01.03.05-employees-promotion', 
    '03.01.01.03.06-employees-branch-transfer', 
    '03.01.01.03.07-employees-resign-termination', 
    '03.01.01.03.08-field-officer-management', 
    '03.01.01.04-samity', 
    '03.01.01.04.01-samity-management', 
    '03.01.01.04.02-samity-transfers', 
    '03.01.01.04.03-samity-field-officer-change', 
    '03.01.01.04.04-samity-batch-field-officer-change', 
    '03.01.01.04.05-samity-day-change', 
    '03.01.01.04.06-samity-closings', 
    '03.01.01.05-member', 
    '03.01.01.05.01-member-management', 
    '03.01.01.05.02-member-samity-transfer', 
    '03.01.01.05.03-member-primary-product-transfer', 
    '03.01.01.05.04-member-closing', 
    '03.01.01.05.05-member-black-list', 
    '03.01.01.05.06-member-attendances', 
    '03.01.01.05.07-member-pass-book-sale', 
    '03.01.01.06-products-accounts', 
    '03.01.01.06.01-manage-loan-products', 
    '03.01.01.06.02-manage-savings-products', 
    '03.01.01.06.03-manage-loan-accounts', 
    '03.01.01.06.04-manage-savings-accounts', 
    '03.01.01.07-transaction', 
    '03.01.01.07.01-disburse-regular-loan', 
    '03.01.01.07.02-disburse-one-time-loan', 
    '03.01.01.07.03-repayment-regular-loan', 
    '03.01.01.07.04-repayment-one-time-loan', 
    '03.01.01.07.05-collect-overdue-loan', 
    '03.01.01.07.06-loan-rebates', 
    '03.01.01.07.07-loan-waive-death', 
    '03.01.01.07.08-loan-adjustment', 
    '03.01.01.07.09-loan-writt-off-eligible-list', 
    '03.01.01.07.010-loan-write-off', 
    '03.01.01.07.011-loan-write-off-collection', 
    '03.01.01.08-process', 
    '03.01.01.08.01-transaction-auth', 
    '03.01.01.08.02-transaction-unauth', 
    '03.01.01.08.03-day-end-process', 
    '03.01.01.08.04-month-end-process', 
    '03.01.01.08.05-pass-book-balance', 
    '03.01.01.08.06-branch-wise-loan-savings', 
    '03.01.01.08.07-consolidated-branch-information'
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

    g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=WORKSHEET_NAMES)
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F')
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