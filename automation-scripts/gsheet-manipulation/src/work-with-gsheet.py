#!/usr/bin/env python3

import json
import yaml
import argparse

from google.google_service import GoogleService
from google.google_sheet import GoogleSheet

from task.resume_tasks import *

from helper.logger import *

def do_something(gsheet):
    # bulk_duplicate_worksheet(gsheet)
    # order_worksheets(gsheet)
    # link_cells_to_worksheet(gsheet)

    # BEGIN resume related
    create_06_job_history_new(gsheet)
    # END   resume related


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to work with")
    args = vars(ap.parse_args())

    if 'gsheet' in args and args["gsheet"] != '':
        gsheet_names = [args["gsheet"]]
    else:
        # read config.yml to get the list of gsheets
        config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
        gsheet_names = config['gsheets']

    google_service = GoogleService('../conf/credential.json')
    for gsheet_name in gsheet_names:
        try:
            info(f"processing .. gsheet {gsheet_name}")
            gsheet = GoogleSheet.open(google_service, gsheet_name=gsheet_name)
            do_something(gsheet)
            info(f"processed  .. gsheet {gsheet_name}")
        except Exception as e:
            warn(str(e))