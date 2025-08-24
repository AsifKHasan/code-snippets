#!/usr/bin/env python3

import os
import multiprocessing
import re
from mutagen.mp4 import MP4, MP4Tags, MP4Cover

from helper.logger import *
from helper.utils import * 

def add_metadata_to_audio(audio_path, data):

    # Get the process ID and name
    current_process_id = os.getpid()
    current_process_name = multiprocessing.current_process().name

    try:
        # Load the MP4 file
        audio = MP4(audio_path)

        # Access the tags and add the metadata
        tags = audio.tags
        tags['\xa9nam'] = [data.get('title', '')]       # Title
        tags['\xa9alb'] = [data.get('album', '')]       # Album
        tags['\xa9ART'] = [data.get('artist', '')]      # Artist
        tags['\xa9gen'] = [data.get('genre', '')]       # Genre
        tags['\xa9day'] = [data.get('date', '')]        # Date

        # Add other common metadata fields
        # if 'album_artist' in data:
        #     tags['aART'] = [data['album_artist']]
        # if 'track_number' in data:
        #     tags['trkn'] = [data['track_number']]
        # if 'comment' in data:
        #     tags['\xa9cmt'] = [data['comment']]
        # if 'composer' in data:
        #     tags['\xa9wrt'] = [data['composer']]
        # if 'lyrics' in data:    
        #     tags['\xa9lyr'] = [data['lyrics']]
        # if 'bpm' in data: 
        #     tags['tmpo'] = [data['bpm']] 
        # if 'disc_number' in data:
        #     tags['disk'] = [data['disc_number']]  
        # if 'grouping' in data:
        #     tags['\xa9grp'] = [data['grouping']]  
        # if 'compilation' in data:
        #     tags['cpil'] = [data['compilation']]  
        # if 'artwork' in data:
        #     with open(data['artwork'], 'rb') as img_file:
        #         img_data = img_file.read()
        #     tags['covr'] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)] 
        
        # Save the changes to the file
        audio.save()
        debug(f"[{current_process_name}]:[{current_process_id}] - [{data['output-audio']}] metadata added")

    except Exception as e:
        print(f"Error adding metadata: {e}")
