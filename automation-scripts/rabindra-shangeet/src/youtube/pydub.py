#!/usr/bin/env python3

import os
import multiprocessing
import re
from pathlib import Path
from pydub import AudioSegment

from helper.logger import *
from helper.utils import * 
from youtube.mutagen import *

def segment_and_tag(data):

    # Get the process ID and name
    current_process_id = os.getpid()
    current_process_name = multiprocessing.current_process().name

    if os.path.exists(data['output-audio']):
        warn(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] exists ... skipping")
        return

    try:
        debug(f"[{current_process_name}]:[{current_process_id}] - [{data['input-audio']}] -> [{data['output-audio']}]")
        # 1. Extract the audio segment and save to a temporary file
        start_ms = hms_to_ms(data['start'])
        end_ms = hms_to_ms(data['end'])
        input_path = data['input-audio']
        # audio = AudioSegment.from_file(input_path, format="mp4")
        audio = AudioSegment.from_file(input_path)
        if end_ms:
            segment = audio[start_ms:end_ms]
        else:
            # Slice from the start time to the end of the audio
            segment = audio[start_ms:]
        
        segment.export(data['output-audio'], format="mp4")
        # segment.export(data['output-audio'])
        debug(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] segment extracted")

        # 2. Add metadata to the temporary file
        add_metadata_to_audio(data['output-audio'], data)

        # 3. Rename the temporary file to the final output file
        # os.rename(temp_file, output_file)
        # print(f"Temporary file renamed to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
