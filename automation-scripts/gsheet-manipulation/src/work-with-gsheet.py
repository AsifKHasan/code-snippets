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

# work specs for applying on a list of worksheets
RANGE_WORK_SPECS = {
    # change fonts and vertical alignments for the worksheet
    # 'A1:Z' : {'font-family': 'Arial', 'font-size': 10, 'valign': 'top'},

    # link -toc-new at cell A1 and left align the cell
    # 'A1' : {'value': '-toc-new', 'ws-name-to-link': '-toc-new', 'weight': 'normal', 'halign': 'left'},

    # change -toc-new
    # 'F3' : {'value': '00-layout', 'ws-name-to-link': '00-layout'},
    # 'F3' : {'value': '00-layout-RHD-TMC', 'ws-name-to-link': '00-layout-RHD-TMC'},

    'C3' : {'value': 'Yes'},
    'C4' : {'value': 'Yes'},
    'C5' : {'value': 'Yes'},
    'C6' : {'value': 'Yes'},

    'D3' : {'value': '1'},
    'D4' : {'value': '2'},
    'D5' : {'value': '2'},
    'D6' : {'value': '2'},

    'G3' : {'value': ''},
    'G4' : {'value': 'section'},
    'G5' : {'value': 'section'},
    'G6' : {'value': 'section'},

    'K3' : {'value': ''},
    'K4' : {'value': ''},
    'K5' : {'value': ''},
    'K6' : {'value': ''},

    'L3' : {'value': 'Yes'},
    'L4' : {'value': ''},
    'L5' : {'value': ''},
    'L6' : {'value': ''},
}

# find and replace patterns
REPLACE_WITH_PATTERNS = [
    {'find': '/data/spectrum/pmo-project-datasheet/', 'replace-with': '/data/organization/01-spectrum/pmo-project-datasheet/'},
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

def work_on_gsheet(g_sheet, g_service, worksheet_names, destination_gsheet_names):

    # worksheet duplication, removal, renaming
    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=worksheet_names)
    # g_sheet.remove_worksheets(worksheet_names_to_remove=worksheet_names)
    # g_sheet.rename_worksheet(worksheet_name='00-layout', new_worksheet_name='00-layout-WB')

    # worksheet creation, formatting and related tasks
    # create_worksheets(g_sheet=g_sheet, worksheet_name_list=worksheet_names)
    # format_worksheets(g_sheet=g_sheet, worksheet_name_list=worksheet_names)

    # trailing blank row removal, review-notes, column size in row 1
    # create_review_notes_conditional_formatting(g_sheet=g_sheet, worksheet_name_list=worksheet_names)
    # g_sheet.remove_extra_columns(worksheet_names=worksheet_names, cols_to_remove_from='F', cols_to_remove_to='end')
    # g_sheet.remove_trailing_blank_rows(worksheet_names=worksheet_names)
    # g_sheet.column_pixels_in_top_row(worksheet_names=worksheet_names)

    # work on ranges etc.
    # g_sheet.work_on_ranges(worksheet_names=worksheet_names, range_work_specs=RANGE_WORK_SPECS)

    # find and replace in worksheets
    # g_sheet.find_and_replace(worksheet_names=worksheet_names, find_replace_patterns=REPLACE_WITH_PATTERNS)

    # for worksheet_name in worksheet_names:
    #     num_rows, num_cols = g_sheet.number_of_dimesnions(worksheet_name=worksheet_name)
    #     if num_rows > 6:
    #         print(f"{g_sheet.title:<30}: [{worksheet_name:<50}] : {num_cols} columns, {num_rows} rows")

    # cell linking and ordering
    g_sheet.link_cells_based_on_type(worksheet_name='-toc-new', range_specs_for_cells_to_link=['E3:F', 'O3:O', 'R3:R'])
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_specs_for_cells_to_link=['F3:F', 'O3:O', 'R3:R'])
    # g_sheet.link_cells_to_drive_files(worksheet_name='-toc-new', range_specs_for_cells_to_link=['F20:F21', 'F24:F26', 'F32:F33', 'F45:F56', 'F59:F63', 'F68:F92', 'F95:F104'])
    g_sheet.order_worksheets()


    # copy worksheets to another gsheet
    # for destination_gsheet_name in destination_gsheet_names:
    #     destination_gsheet = g_service.open(gsheet_name=destination_gsheet_name)
    #     if destination_gsheet:
    #         for worksheet_name in worksheet_names:
    #             g_sheet.copy_worksheet_to_gsheet(destination_gsheet=destination_gsheet, worksheet_name_to_copy=worksheet_name)


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

    # read config.yml to get the list of gsheets and other data
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    if 'gsheet' in args and args["gsheet"] != '':
        gsheet_names = [args["gsheet"]]
    else:
        gsheet_names = config['gsheets']

    destination_gsheet_names = config['destination-gsheets']
    worksheet_names = config['worksheets']

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
            work_on_gsheet(g_sheet=g_sheet, g_service=g_service, worksheet_names=worksheet_names, destination_gsheet_names=destination_gsheet_names)
            # work_on_drive(g_service=g_service, g_sheet=g_sheet)
            info(f"processed  {count:>4}/{num_gsheets} gsheet {gsheet_name}\n")

        wait_for = 30
        if count % 500 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)
