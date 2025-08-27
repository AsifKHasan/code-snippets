#!/usr/bin/env python3

from pydub import AudioSegment

# Load the m4a file
audio_file = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/f_Di2ycg6z4.m4a'
audio = AudioSegment.from_file(audio_file)

# Convert to 16-bit mono PCM and resample to 16000 Hz
audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

# Get the raw audio data
raw_audio_data = audio.raw_data



import webrtcvad
import struct

# Create a VAD instance with an aggressiveness level (0-3)
vad = webrtcvad.Vad(3)

# Frame duration in milliseconds (WebRTC VAD supports 10, 20, 30)
frame_duration_ms = 30
sample_rate = 16000
samples_per_frame = int(sample_rate * frame_duration_ms / 1000)
bytes_per_sample = 2

# Iterate through the raw audio data and check for speech
start_time = None
for i in range(0, len(raw_audio_data), samples_per_frame * bytes_per_sample):
    frame = raw_audio_data[i:i + samples_per_frame * bytes_per_sample]
    
    # Ensure the frame has the expected number of samples
    if len(frame) < samples_per_frame * bytes_per_sample:
        continue
    
    is_speech = vad.is_speech(frame, sample_rate)
    
    if is_speech and start_time is None:
        start_time = (i / bytes_per_sample) / sample_rate
        print(f"Human voice starts at: {start_time:.2f} seconds")
        break

if start_time is None:
    print("No human voice detected.")