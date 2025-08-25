#!/usr/bin/env python

# import os
# import json
import yaml
import argparse
import multiprocessing
from functools import partial
from pathlib import Path

from ggle.google_service import GoogleService

from youtube.yt_dlp import *
from helper.logger import *
from helper import logger

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--youtube", required=False, help="youtube url to download from")
    args = vars(ap.parse_args())

    # read config.yml
    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    config_path = Path(config_path).resolve()
    logger.LOG_LEVEL = config.get('log-level', 0)
    credential_json = config['credential-json']
    gsheet_name = config.get('gsheet')
    worksheet_name = config.get('worksheet')
    output_dir = config.get('output-dir')
    extract_pool_size = config.get('extract-pool-size', 2)

    if args["youtube"] is not None:
        video_url = args["youtube"]
        id = video_url.replace('https://www.youtube.com/watch?v=', '')
        data = {'url': video_url, 'id': id, 'output-dir': output_dir}
        check_and_download(data)
    else:
        g_service = GoogleService(credential_json)
        try:
            info(f"processing gsheet {gsheet_name}")
            g_sheet = g_service.open(gsheet_name=gsheet_name)
        except Exception as e:
            g_sheet = None
            warn(str(e))
            # raise e

        if g_sheet:
            worksheet = g_sheet.worksheet_by_name(worksheet_name)
            values = worksheet.get_values_in_batch(ranges=['A4:P'])

            data_list = []
            for value in values[0]:
                if value[5] == 'Yes' and value[7] != '':
                    # get id from url, if there is a file with that id, skip it
                    id = re.sub(r"&.+", "", value[12])

                    output_path = f"{output_dir}{id}.m4a"
                    if os.path.exists(output_path):
                        warn(f"[{output_path}] exists ... skipping")
                    else:
                        data_list.append({'url': value[7], 'id': id, 'output-dir': output_dir})

            with multiprocessing.Pool(processes=extract_pool_size) as pool:
                # Use pool.map to apply the worker_function to each item
                results = pool.map(check_and_download, data_list)
