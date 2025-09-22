#!/usr/bin/env python3

import librosa
import numpy as np

def detect_voice_segments(audio_path, frame_size=0.02, min_voice_duration=0.1):
    """
    Detects voice segments in an audio file using MFCCs.

    Args:
        audio_path (str): The path to the audio file.
        sr (int): The sample rate of the audio.
        frame_size (float): The duration of each audio frame in seconds.
        min_voice_duration (float): The minimum duration of a voice segment to be considered valid.

    Returns:
        list: A list of tuples, where each tuple contains the start and end time
              (in seconds) of a detected voice segment.
    """
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Calculate the number of samples per frame
    frame_length = int(frame_size * sr)
    
    # Calculate MFCCs
    # We'll use a small window and hop length to get more granularity
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=1, n_fft=frame_length, hop_length=frame_length)
    
    # The first MFCC (MFCC 0) is a good indicator of energy
    # We'll use a simple threshold on the average MFCC 0 to detect voice
    # This threshold might need to be adjusted based on your audio
    mfcc0_mean = np.mean(mfccs)
    mfcc0_std = np.std(mfccs)
    threshold = mfcc0_mean + mfcc0_std / 2
    
    # Find frames where MFCC 0 is above the threshold
    voice_frames = mfccs[0] > threshold
    
    voice_segments = []
    in_voice = False
    start_frame = 0

    # Iterate through frames to find continuous voice segments
    for i, is_voice in enumerate(voice_frames):
        if is_voice and not in_voice:
            in_voice = True
            start_frame = i
        elif not is_voice and in_voice:
            end_frame = i
            # Convert frame numbers to time in seconds
            start_time = start_frame * frame_size
            end_time = end_frame * frame_size
            
            # Filter out very short segments that are likely not voice
            if (end_time - start_time) > min_voice_duration:
                voice_segments.append((start_time, end_time))
            
            in_voice = False
    
    # Handle case where voice continues until the end of the file
    if in_voice:
        start_time = start_frame * frame_size
        end_time = len(y) / sr
        if (end_time - start_time) > min_voice_duration:
            voice_segments.append((start_time, end_time))
            
    return voice_segments

# Example usage:
audio_file = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/f_Di2ycg6z4.m4a'
try:
    voice_starts = detect_voice_segments(audio_file)
    if voice_starts:
        print("Detected voice segments:")
        for start, end in voice_starts:
            print(f"  - Voice starts at {start:.2f}s and ends at {end:.2f}s")
    else:
        print("No voice segments detected.")
except Exception as e:
    print(f"An error occurred: {e}")