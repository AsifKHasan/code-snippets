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

DESTINATION_GSHEETS = [
    'NBR-USAID-FFBT-ARDS__volume-1__technical-proposal__spectrum',
]

WORKSHEET_NAMES = [
    # 'z-blank',

    '01-methodology-and-work-plan',
    '01.01-project-work-plan',
    '01.01.01-kick-off-plan-with-whole-team',
    '01.01.02-implementation-management',
    '01.01.03-risk-management-plan',
    '01.01.04-quality-assurance',
    '01.01.05-communication-plan',
    '01.01.06-change-management-plan',
    '01.01.07-uat-build-release-and-deployment-plan',

    'A-sow-understanding',
    'B-proposed-solution',
    'B.01-proposed-architecture',
    'B.01.01-containerized-architecture',
    'B.01.02-modular-architecture',
    'B.01.03-safety-redundancy',
    'B.01.04-interoperability',
    'B.01.05-performance',
    'B.01.06-user-interface-experience',
    'B.01.07-ease-of-maintenance',
    'B.01.08-architectural-scalability',
    'B.01.09-information-security',
    'B.01.10-business-continuity',
    'B.01.11-state-integrity',
    'B.02-proposed-technology-stack',
    'B.03-deployment-and-delivery',
    'B.03.01-environment-deployment-flow',
    'B.03.02-technical-deliverables-list',
    'B.03.03-usage-model-licensing',
    'B.04-warranty-support',
    'C-compliance-commentary',
    'C.01-general-functional-compliance',
    'C.02-functional-compliance',

    # 'C.02.01-user-registration-management',
    # 'C.02.02-user-dashboard',
    # 'C.02.03-appeal-application-management',
    # 'C.02.04-field-office-management',
    # 'C.02.05-appeal-operation-management',
    # 'C.02.06-report-management',
    # 'C.02.07-monitoring-management',
    # 'C.02.08-security-management',
    # 'C.02.09-system-log-management',
    # 'C.02.10-backup-management',
    # 'C.02.11-restore-archive-management',

    'C.03-non-functional-compliance',
    'C.03.01-licensing-intellectual-property',
    'C.03.02-system-architecture',
    'C.03.03-interoperability',
    'C.03.04-performance',
    'C.03.05-flexibility',
    'C.03.06-user-interface-ergonomics',
    'C.03.07-maintenance',
    'C.03.08-scalability',
    'C.03.09-information-security',
    'C.03.10-resilience-continuity',
    'C.04-warranty-support-conditions',
    'C.05-deliverables-list',

]

RANGE_WORK_SPECS = {
        'A1:I' : {'font-family': 'Times New Roman', 'font-size': 12, 'valign': 'top'}
}

def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related

    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')

    # END   drive file related
    pass


def work_on_gsheet(g_sheet, g_service):

    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=WORKSHEET_NAMES)
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F21')
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F28:F28')
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F41:F')
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='O3:O')
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='R3:R')
    g_sheet.order_worksheets()

    # for ws_name in WORKSHEET_NAMES:
        # g_sheet.remove_worksheet(worksheet_name=ws_name)

    # g_sheet.rename_worksheet(worksheet_name='06-job-history-ffbt', new_worksheet_name='06-job-history-USAID-FFBT')

    # copy worksheets to another gsheet
    destination_gsheet = g_service.open(DESTINATION_GSHEETS[0])
    if destination_gsheet:
        for worksheet_name in WORKSHEET_NAMES:
            # g_sheet.copy_worksheet_to_gsheet(destination_gsheet, worksheet_name_to_copy=worksheet_name)
            pass


    for worksheet_name in WORKSHEET_NAMES:
        # g_sheet.work_on_ranges(worksheet_name=worksheet_name, range_work_specs=RANGE_WORK_SPECS)
        # g_sheet.remove_trailing_blank_rows(worksheet_name='-toc-new')
        pass

    for worksheet_name in WORKSHEET_NAMES:
        # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name)
        # print(f"{g_sheet.title:<30}: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")
        pass


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
        if count % 10 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)
