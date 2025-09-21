#!/usr/bin/env python3

import os
import multiprocessing
import re
from pathlib import Path
import subprocess

import ffmpeg

# import asyncio
# from ffmpeg import Progress
# from ffmpeg.asyncio import FFmpeg

from helper.logger import *
from helper.utils import * 
from audio.mutagen import *

def segment_and_tag(data):
# def segment_and_tag_subprocess(data):
    # Get the process ID and name
    current_process_id = os.getpid()
    current_process_name = multiprocessing.current_process().name

    if os.path.exists(data['output-audio']):
        warn(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] exists ... skipping")
        return

    debug(f"[{current_process_name}]:[{current_process_id}] - [{data['input-audio']}] -> [{data['output-audio']}]")
    start_time = data['start']
    end_time = data['end']
    command = [
        'ffmpeg',
        '-i', data['input-audio'],
        '-ss', str(start_time),
    ]
    if end_time != '':
        command.extend(['-to', str(end_time)])

    for key, value in data.items():
        if key in ['title', 'artist', 'album', 'genre', 'date', 'comment', 'lyrics']:
            command.extend(['-metadata', f'{key}={value}'])
    
    command.extend([data['output-audio']])

    try:
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


# def segment_and_tag(data):
def segment_and_tag_sync(data):
    # Get the process ID and name
    current_process_id = os.getpid()
    current_process_name = multiprocessing.current_process().name

    if os.path.exists(data['output-audio']):
        warn(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] exists ... skipping")
        return

    try:
        debug(f"[{current_process_name}]:[{current_process_id}] - [{data['input-audio']}] -> [{data['output-audio']}]")
        start_time = data['start']
        end_time = data['end']
        if end_time != '':
            (
                ffmpeg
                .input(data['input-audio'], ss=start_time, to=end_time)
                .output(
                    data['output-audio'],
                    **{'metadata:s:v:0': f"title='{data['title']}'",
                       'metadata:s:a:0': f'artist={data["artist"]}',
                       'metadata:g': f'album={data["album"]}',
                       'metadata:g': f'genre={data["genre"]}',
                       'metadata:g': f'date={data["date"]}'}
                )
                .run(overwrite_output=True)
            )
        else:
            (
                ffmpeg
                .input(data['input-audio'], ss=start_time)
                .output(data['output-audio'],
                    **{'metadata:s:v:0': f"title='{data['title']}'",
                       'metadata:s:a:0': f'artist={data["artist"]}',
                       'metadata:g': f'album={data["album"]}',
                       'metadata:g': f'genre={data["genre"]}',
                       'metadata:g': f'date={data["date"]}'}
                )
                .run(overwrite_output=True)
            )

        debug(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] audio transcoded")

    except Exception as e:
        print(f"An error occurred: {e}")
