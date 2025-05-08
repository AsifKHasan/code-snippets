#!/usr/bin/env python3

import os
from pytube import YouTube
from helper.logger import *

def download_youtube_audio(url, output_path='.'):
    """Downloads the audio of a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str, optional): The directory to save the audio. Defaults to the current directory.
    """
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            print(f"Downloading audio from: {yt.title}")
            out_file = audio_stream.download(output_path=output_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(f"Audio downloaded successfully to: {new_file}")
        else:
            print("No audio stream found for this video.")

    except Exception as e:
        print(f"An error occurred: {e}")
