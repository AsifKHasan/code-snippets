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
DESTINATION_GSHEET_NAMES = [
]

# list of worksheets on which to do a common work
WORKSHEET_NAMES = [
    # '-toc-new',
    # '00-layout',
    # '01-personal',
    # '02-career-highlight',
    # '03-education',
    # '04-managerial-expertise',
    # '05-technical-expertise',
    # '06-job-history',
    # '07-project-roles',
    # '08-training',
    # '09-certification',
    # '10-membership',
    # '11-language-proficiency',
    # '12-contact',
    # '13-educational-certificates',
    # '14-vendor-certificates',
    # '15-institutional-certificates',
    # '16-references',
    # 'z-footer',
    # 'z-header',
]

# work specs for applying on a list of worksheets
RANGE_WORK_SPECS = {
    # change fonts and vertical alignments for the worksheet
    # 'A1:Z' : {'font-family': 'Arial', 'font-size': 10, 'valign': 'top'},
    # link -toc-new at cell A1 and left align the cell
    # 'A1' : {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'weight': 'normal', 'halign': 'left'},
}

# find and replace patterns
REPLACE_WITH_PATTERNS = [
    # {'find': '/doer/', 'replace-with': '/03-doer/'},
    # {'find': '/diploma/', 'replace-with': '/01-diploma/'},
    # {'find': '/bachelor/', 'replace-with': '/02-bachelor/'},
    # {'find': '/master/', 'replace-with': '/03-master/'},

    # {'find': '/01-diploma/03-doer/', 'replace-with': '/03-doer/01-diploma/'},
    # {'find': '/02-bachelor/03-doer/', 'replace-with': '/03-doer/02-bachelor/'},
    # {'find': '/03-master/03-doer/', 'replace-with': '/03-doer/03-master/'},
    #
    # {'find': '/udemy/03-doer/', 'replace-with': '/03-doer/udemy/'},
    # {'find': '/coursera/03-doer/', 'replace-with': '/03-doer/coursera/'},
    #
    # {'find': '/institutional-certificates/', 'replace-with': '/institutional-certificates/03-doer/'},
    # {'find': '/vendor-certificates/', 'replace-with': '/vendor-certificates/03-doer/'},
]

def work_on_gsheet(g_sheet, g_service):

    # worksheet duplication, removal, renaming
    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=WORKSHEET_NAMES)
    # g_sheet.remove_worksheets(worksheet_names_to_remove=WORKSHEET_NAMES)
    # g_sheet.rename_worksheet(worksheet_name='06-job-history-ffbt', new_worksheet_name='06-job-history-USAID-FFBT')

    # worksheet creation, formatting and related tasks
    # create_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # format_worksheets(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)

    # trailing blank row removal, review-notes, column size in row 1
    # create_review_notes_conditional_formatting(g_sheet=g_sheet, worksheet_name_list=WORKSHEET_NAMES)
    # g_sheet.remove_trailing_blank_rows(worksheet_names=WORKSHEET_NAMES)
    # g_sheet.column_pixels_in_top_row(worksheet_names=WORKSHEET_NAMES)

    # work on ranges etc.
    # g_sheet.work_on_ranges(worksheet_names=WORKSHEET_NAMES, range_work_specs=RANGE_WORK_SPECS)

    # find and replace in worksheets
    # g_sheet.find_and_replace(worksheet_names=WORKSHEET_NAMES, find_replace_patterns=REPLACE_WITH_PATTERNS)

    # for worksheet_name in WORKSHEET_NAMES:
        # num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name)
        # print(f"{g_sheet.title:<30}: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")

    # cell linking and ordering
    # g_sheet.link_cells_to_drive_files(worksheet_name='-toc-new', range_specs_for_cells_to_link=['F20:F21', 'F24:F26', 'F32:F33', 'F45:F56', 'F59:F63', 'F68:F92', 'F95:F104'])
    g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_specs_for_cells_to_link=['F3:F19', 'F23:F23', 'F28:F31', 'F35:F44', 'F58:F58', 'F65:F65', 'F67:F67', 'F94:F94', 'O3:O', 'R3:R'])
    # g_sheet.order_worksheets()


    # copy worksheets to another gsheet
    # for destination_gsheet_name in DESTINATION_GSHEET_NAMES:
    #     destination_gsheet = g_service.open(gsheet_name=destination_gsheet_name)
    #     if destination_gsheet:
    #         for worksheet_name in WORKSHEET_NAMES:
    #             g_sheet.copy_worksheet_to_gsheet(destination_gsheet=destination_gsheet, worksheet_name_to_copy=worksheet_name)
    #             pass


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


def work_on_drive(g_service, g_sheet):

    # BEGIN drive file related

    # target_file_id = g_service.copy_file(source_file_id=g_sheet.id(), target_folder_id='1Ol7pNkAloXNPxeU8j1_IMNAayUh7AvPf', target_file_title='BNDA__standards')
    # g_service.share(file_id=target_file_id, email='asif.hasan@gmail.com', perm_type='user', role='owner')
    # g_service.share(file_id='1J7VpUFfZiQi543f4zdGcX9mqX7HugvsmebtoECCgk_4', email='asif.hasan@gmail.com', perm_type='user', role='owner')

    # END   drive file related
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

        wait_for = 30
        if count % 500 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)
