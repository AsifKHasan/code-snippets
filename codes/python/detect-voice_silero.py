#!/usr/bin/env python3

from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pprint import pprint

audio_file = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/f_Di2ycg6z4.m4a'

model = load_silero_vad()
wav = read_audio(audio_file)
speech_timestamps = get_speech_timestamps(
  wav,
  model,
  return_seconds=True,  # Return speech timestamps in seconds (default is samples)
)
pprint(speech_timestamps)