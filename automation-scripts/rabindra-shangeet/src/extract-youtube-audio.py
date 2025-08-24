#!/usr/bin/env python

# import os
# import json
import yaml
import argparse
import multiprocessing
from functools import partial
from pathlib import Path

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
    output_dir = config.get('output-dir')
    extract_pool_size = config.get('extract-pool-size', 2)

    if args["youtube"] is not None:
        video_url = [args["youtube"]]
        check_and_download(video_url, output_path=output_dir)
    else:
        video_urls = config.get('links-to-open', [])
        process_partial = partial(check_and_download, output_path=output_dir)

        with multiprocessing.Pool(processes=extract_pool_size) as pool:
            # Use pool.map to apply the worker_function to each item
            results = pool.map(process_partial, video_urls)
