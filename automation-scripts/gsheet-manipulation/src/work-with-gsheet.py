#!/usr/bin/env python3

import json
import yaml
import time
import argparse

from google.google_service import GoogleService
from google.google_sheet import GoogleSheet

from task.resume_tasks import *

from helper.logger import *


def do_something(gsheet):

    # gsheet.bulk_duplicate_worksheet(worksheet_name_to_duplicate='z-blank', new_worksheet_names=['04.01-৩১', '04.01-৩২', '04.02-৩৩', '04.02-৩৪', '04.03-৩৫', '04.03-৩৬'])
    # gsheet.link_cells_to_worksheet(worksheet_name='-toc-new', range_spec_for_cells_to_link='F3:F')

    # gsheet.rename_worksheet(worksheet_name='06-job-history', new_worksheet_name='06-job-history-Z')
    # gsheet.rename_worksheet(worksheet_name='06-job-history-NEW', new_worksheet_name='06-job-history')
    # gsheet.order_worksheets()

    # gsheet.work_on_ranges(worksheet_name='-toc-new', range_work_specs={'F3': {'value': '00-layout', 'ws-name-to-link': '00-layout'}})
    # gsheet.work_on_ranges(worksheet_name='00-layout', range_work_specs={'B29': {'value': '06-job-history', 'ws-name-to-link': '06-job-history', 'note': '{"content": "out-of-cell"}'}})

    # gsheet.remove_worksheet(worksheet_name='-toc')
    # gsheet.remove_worksheet(worksheet_name='06-job-history-Z')
    # gsheet.remove_worksheet(worksheet_name='07-project-roles-Z')
    # gsheet.order_worksheets()


    # BEGIN resume related
    # create_06_job_history_new(gsheet)
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
            info(f"{count:>4}/{num_gsheets} : processing .. gsheet {gsheet_name}")
            gsheet = GoogleSheet.open(google_service, gsheet_name=gsheet_name)
        except Exception as e:
            gsheet = None
            warn(str(e))
            # raise e

        if gsheet:
            do_something(gsheet)
            info(f"{count:>4}/{num_gsheets} : processed  .. gsheet {gsheet_name}\n")

        wait_for = 50
        if count % 5 == 0:
            warn(f"sleeping for {wait_for} seconds\n")
            time.sleep(wait_for)