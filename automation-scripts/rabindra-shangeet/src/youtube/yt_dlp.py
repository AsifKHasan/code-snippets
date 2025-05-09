#!/usr/bin/env python3

import os
import yt_dlp
from helper.logger import *

def check_and_download(url, output_path='.'):
    # check if the audio is already downloaded or not
    id = get_youtube_id(url)
    file_path = f"{output_path}/{id}.m4a"

    if os.path.exists(file_path):
        warn(f"The audio '{file_path}' exists ... skipping")
    else:
        debug(f"Downloading audio '{file_path}'")

        if id:
            download_audio(url, output_path)


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
        error(f"An error occurred: {e}")
        return None


def download_audio(url, output_path):
    ydl_opts = {
        'extractaudio': True,
        'audioformat': 'm4a',
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_path, '%(id)s.m4a'),
        'verbose': False,
        'quiet': True,
        'starttime': 6,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        info(f"Audio downloaded to: {output_path}")

    except Exception as e:
        error(f"An error occurred: {e}")



