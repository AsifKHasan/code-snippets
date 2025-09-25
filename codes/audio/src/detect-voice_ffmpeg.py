#!/usr/bin/env python

import webrtcvad
import collections
import wave
import contextlib
import subprocess

# Step 1: convert m4a -> wav (mono, 16kHz, 16bit PCM)
# Requires ffmpeg installed on your system
input_audio = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/f_Di2ycg6z4.m4a'
output_audio = '/tmp/converted.wav'
subprocess.run([
    "ffmpeg", "-y", "-i", input_audio,
    "-ac", "1",              # mono
    "-ar", "16000",          # 16 kHz
    "-f", "wav", output_audio
])

# Helper to read audio frames
def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)  # 2 bytes per sample
    offset = 0
    while offset + n <= len(audio):
        yield audio[offset:offset + n]
        offset += n

# Step 2: Run VAD
vad = webrtcvad.Vad(3)  # aggressiveness: 0–3
audio, sample_rate = read_wave(output_audio)

frames = list(frame_generator(30, audio, sample_rate))  # 30 ms frames recommended

# Step 3: Find first voiced frame
start_time = None
for i, frame in enumerate(frames):
    is_speech = vad.is_speech(frame, sample_rate)
    if is_speech:
        start_time = i * 0.03  # each frame is 30 ms
        break

if start_time is not None:
    print(f"Voice starts at ~{start_time:.2f} seconds")
else:
    print("No speech detected")
