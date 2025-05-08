#!/usr/bin/env python3

import os
import youtube_dl
from helper.logger import *

def download_youtube_audio(url, output_path='.'):
    ydl_opts = {
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True, # Ensure it only downloads a single video
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Audio downloaded successfully to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
