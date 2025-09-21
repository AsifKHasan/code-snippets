#!/usr/bin/env python

# import os
import json
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

LYRIC_COL = 0
ID_COL = 1
YEAR_COL = 2
GENRE_COL = 5
DO_COL = 7
TITLE_COL = 8
URL_COL = 9
ARTIST_COL = 10
START_COL = 11
END_COL = 12
SOURCE_FILE_COL = 14
TARGET_FILE_COL = 17

def get_the_lyrics():
    lyrics_dict = {}
    return lyrics_dict

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
    song_data_file = config.get('song-data-file')

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
        values = worksheet.get_values_in_batch(ranges=['A4:R'])

        data_list = []
        # get the lyrics
        with open(song_data_file, 'r') as json_file:
            songs = json.loads(json_file.read())

        for value in values[0]:
            if value[DO_COL] == 'Yes' and value[URL_COL] != '':
                # lyrics are keyed by id in column A
                lyrics = songs.get(value[ID_COL])
                data = {
                    'input-audio': f"{input_audio_dir}{value[SOURCE_FILE_COL]}.m4a",
                    'output-audio': f"{tagged_audio_dir}{value[TARGET_FILE_COL]}.m4a",
                    'start': str(value[START_COL]),
                    'end': str(value[END_COL]),
                    'title': value[TITLE_COL],
                    'date': str(value[YEAR_COL]),
                    'artist': value[ARTIST_COL],
                    'album': 'রবীন্দ্রসঙ্গীত',
                    'genre': value[GENRE_COL],
                    'lyrics': lyrics,
                    'comment': lyrics,
                }

                data_list.append(data)

        # process_partial = partial(segment_and_tag, output_path=tagged_audio_dir)

        with multiprocessing.Pool(processes=tag_pool_size) as pool:
            # Use pool.map to apply the worker_function to each item
            results = pool.map(segment_and_tag, data_list)

