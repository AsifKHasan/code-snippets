#!/usr/bin/env python

# import os
# import json
import yaml
import argparse
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
    # output_directory = f"{config_path.parent}/{config.get('output-dir')}"
    output_directory = config.get('output-dir')

    if args["youtube"] is not None:
        video_urls = [args["youtube"]]
    else:
        video_urls = config.get('links-to-open', [])

    for video_url in video_urls:
        check_and_download(video_url, output_directory)
