#!/usr/bin/env python

# import os
# import json
import yaml
import argparse
import multiprocessing
from functools import partial
from pathlib import Path

from ggle.google_service import GoogleService

from audio.ffmpeg import *
# from audio.pydub import *
# from audio.mutagen import *

from helper.utils import *
from helper.logger import *
from helper import logger

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    args = vars(ap.parse_args())

    # read config.yml
    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    config_path = Path(config_path).resolve()
    logger.LOG_LEVEL = config.get('log-level', 0)
    credential_json = config['credential-json']
    gsheet_name = config.get('gsheet')
    worksheet_name = config.get('worksheet')
    input_audio_dir = config.get('input-audio-dir')
    tagged_audio_dir = config.get('tagged-audio-dir')
    tag_pool_size = config.get('tag-pool-size', 2)

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
                # TODO: fix lyrics and comment
                lyrics = 'অকারণে অকালে মোর পড়ল যখন ডাক\n    তখন আমি ছিলেম শয়ন পাতি।'
                data = {
                    'input-audio': f"{input_audio_dir}{value[12]}.m4a",
                    'output-audio': f"{tagged_audio_dir}{value[15]}.m4a",
                    'start': str(value[9]),
                    'end': str(value[10]),
                    'title': value[6],
                    'date': str(value[0]),
                    'artist': value[8],
                    'album': 'রবীন্দ্রসঙ্গীত',
                    'genre': value[3],
                    'lyrics': lyrics,
                    'comment': lyrics,
                }

                data_list.append(data)

        # process_partial = partial(segment_and_tag, output_path=tagged_audio_dir)

        with multiprocessing.Pool(processes=tag_pool_size) as pool:
            # Use pool.map to apply the worker_function to each item
            results = pool.map(segment_and_tag, data_list)

