#!/usr/bin/env python3

import webrtcvad
from pydub import AudioSegment
import numpy as np

def find_voice_segments(audio_path, aggressiveness=3):
    """
    Finds voice segments in an audio file using py-webrtcvad.

    Args:
        audio_path (str): The path to the audio file.
        aggressiveness (int): The VAD aggressiveness mode (0-3).

    Returns:
        list: A list of tuples (start_time, end_time) in seconds.
    """
    try:
        # Load and convert audio to the required format
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        raw_audio = audio.raw_data
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return []

    vad = webrtcvad.Vad(aggressiveness)
    
    frame_duration_ms = 10  # Can be 10, 20, or 30
    frame_size_bytes = int(frame_duration_ms * 16000 / 1000) * 2
    
    voice_segments = []
    current_segment_start = None

    for i in range(0, len(raw_audio), frame_size_bytes):
        frame = raw_audio[i:i + frame_size_bytes]
        if len(frame) < frame_size_bytes:
            continue

        is_speech = vad.is_speech(frame, 16000)
        current_time = (i / frame_size_bytes) * frame_duration_ms / 1000.0

        if is_speech:
            if current_segment_start is None:
                current_segment_start = current_time
        else:
            if current_segment_start is not None:
                voice_segments.append((current_segment_start, current_time))
                current_segment_start = None

    # Handle a final segment that goes to the end of the file
    if current_segment_start is not None:
        voice_segments.append((current_segment_start, len(raw_audio) / (16000 * 2)))

    return voice_segments

# Example usage
audio_file = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/f_Di2ycg6z4.m4a'
segments = find_voice_segments(audio_file)

if segments:
    print("Detected voice segments:")
    for start, end in segments:
        print(f"  - Voice starts at {start:.2f}s and ends at {end:.2f}s")
else:
    print("No voice detected.")