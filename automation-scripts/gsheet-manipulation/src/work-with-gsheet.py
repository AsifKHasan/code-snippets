#!/usr/bin/env python3

import json
import yaml
import time
import argparse

from google.google_service import GoogleService

from task.resume_tasks import *

from helper.logger import *


def do_something(g_sheet):


    # g_sheet.duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=[])
    # g_sheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F')

    # g_sheet.rename_worksheet(worksheet_name='06-job-history', new_worksheet_name='06-job-history-Z')
    # g_sheet.rename_worksheet(worksheet_name='06-job-history-Z', new_worksheet_name='06-job-history')

    # g_sheet.work_on_ranges(worksheet_name='-toc-new', range_work_specs={'F3': {'value': '00-layout', 'ws-name-to-link': '00-layout'}})
    # g_sheet.work_on_ranges(worksheet_name='00-layout', range_work_specs={'B29': {'value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "out-of-cell"}'}})

    # g_sheet.remove_worksheet(worksheet_name='-toc')
    # g_sheet.remove_worksheet(worksheet_name='06-job-history-Z')
    # g_sheet.remove_worksheet(worksheet_name='07-project-roles-Z')
    # g_sheet.order_worksheets()

    new_toc_from_toc(g_sheet)


    # BEGIN resume related
    # retouch_worksheets(g_sheet)
    # create_06_job_history_new(g_sheet)
    # END   resume related


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

    google_service = GoogleService('../conf/credential.json')
    count = 0
    num_gsheets = len(gsheet_names)
    for gsheet_name in gsheet_names:
        count = count + 1
        try:
            info(f"processing {count:>4}/{num_gsheets} gsheet {gsheet_name}")
            g_sheet = google_service.open(gsheet_name=gsheet_name)
        except Exception as e:
            g_sheet = None
            warn(str(e))
            # raise e

        if g_sheet:
            do_something(g_sheet=g_sheet)
            info(f"processed  {count:>4}/{num_gsheets} gsheet {gsheet_name}\n")

        wait_for = 50
        if count % 5 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)