#!/usr/bin/env python3

# import os
# import json
import yaml
# import time
import argparse

from youtube.yt_dlp import *
from helper.logger import *
from helper import logger

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--youtube", required=True, help="youtube url to download from")
    ap.add_argument("-o", "--output_dir", required=True, help="output directory")
    args = vars(ap.parse_args())

    # read config.yml
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)

    video_url = args["youtube"]
    output_directory = args["output_dir"]
    check_and_download(video_url, output_directory)
