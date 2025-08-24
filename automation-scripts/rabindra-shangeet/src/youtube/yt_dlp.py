#!/usr/bin/env python3

import os
import multiprocessing
import re
import yt_dlp

from helper.logger import *

def check_and_download(data):

    # Get the process ID and name
    current_process_id = os.getpid()
    current_process_name = multiprocessing.current_process().name

    # download the audio
    debug(f"[{current_process_name}]:[{current_process_id}] - downloading [{data['output-dir']}{data['id']}.m4a]")

    if id:
        download_audio(data['url'], data['id'], data['output-dir'], current_process_name, current_process_id)
        # pass


def get_youtube_id(url):
    ydl_opts = {'verbose': False, 'quiet': True}  # You can add other options if needed
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # download=False prevents actual downloading
            if info_dict and 'id' in info_dict:
                return info_dict['id']
            else:
                return None

    except Exception as e:
        error(f"an error occurred: {e}")
        return None


def download_audio(url, id, output_dir, current_process_name, current_process_id):
    ydl_opts = {
        'extractaudio': True,
        'audioformat': 'm4a',
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_dir, '%(id)s.m4a'),
        'verbose': False,
        'quiet': True,
        'starttime': 6,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        info(f"[{current_process_name}]:[{current_process_id}] - downloaded  [{output_dir}{id}.m4a]")

    except Exception as e:
        error(f"[{current_process_name}]:[{current_process_id}] - an error occurred: {e}")
