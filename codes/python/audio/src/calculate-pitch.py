#!/usr/bin/env python

# we may need this to get rid of segfault
# conda install -c conda-forge librosa

import os
import math
import csv
import argparse
import yaml
import warnings
import soundfile
from pydub import AudioSegment
import librosa
import librosa.display
import numpy as np
import multiprocessing
from functools import partial

import matplotlib.pyplot as plt
import matplotlib.style as ms

from helper.utils import *
from helper.logger import *
from helper import logger

warnings.filterwarnings('ignore')

audio_path = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/{}.m4a'
csv_path = '../out/pitch_data__{}.csv'
frame_duration_s = 0.020

def plot_pitch_contour(times, f0):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the F0
    ax.plot(times, f0, label='F0', color='blue', linewidth=2)

    # Set the plot labels and title
    ax.set_title('F0 Contour')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Add a grid for easier reading
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Display the plot
    plt.tight_layout()

    plt.show()


def plot_pitch_spectrogram(y, times, f0):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the spectrogram
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')

    # Plot the F0 contour on top of the spectrogram
    ax.plot(times, f0, label='F0 (PYIN)', color='cyan', linewidth=3)

    ax.set(title='Pitch (F0) analysis with PYIN', xlabel='Time (s)', ylabel='Frequency (Hz)')
    ax.legend(loc='upper right')

    plt.show()


def calculate_pitch(audio_tuple):
    i, audio_name = audio_tuple
    audio_file = audio_path.format(audio_name)
    info(f"{i} {audio_name}: calculating Pitch")

    try:
        # Step 1: Load the audio file
        y, sr = librosa.load(audio_file)
        debug(f"{i} {audio_name}: sampling rate: {sr} Hz", nesting_level=1)
        debug(f"{i} {audio_name}: frame duration: {frame_duration_s * 1000}ms", nesting_level=1)

        # 2. Convert ms values to samples
        # frame_length determines the window size (40ms is common for pitch analysis)
        frame_length = int(sr * frame_duration_s) 
        debug(f"{i} {audio_name}: frame length: {frame_length}", nesting_level=1)

        # Step 2: Calculate the hop_length for a 20ms interval
        # hop_length determines the time resolution of the output (10ms is common)
        hop_length = int(frame_duration_s * sr)
        debug(f"{i} {audio_name}: hop length for 20ms: {hop_length} samples", nesting_level=1)

        # 2. Perform pitch analysis using the PYIN algorithm
        # f0 is the fundamental frequency, voiced_flag is a boolean indicating
        # if the frame is voiced, voiced_probs is the probability of it being voiced.
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), hop_length=hop_length, frame_length=frame_length)

        # 3. Filter out unvoiced frames by replacing their f0 with NaN (Not a Number)
        # This makes plotting cleaner as it creates gaps for silences.
        # times = librosa.times_like(f0)
        # times = librosa.frames_to_time(np.arange(len(f0)), sr=sr)
        times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)
        f0[~voiced_flag] = np.nan

        info(f"{i} {audio_name}: successfully calculated Pitch")


        # Create a dictionary of the data
        data = {
            'time': times,
            'f0': f0,
            # Convert boolean to integer (1 or 0)
            'voiced': voiced_flag.astype(int),
            'probability': voiced_probs
        }

        save_dict_as_csv(csv_path=csv_path.format(audio_name), data=data)

        plot_pitch_contour(times=times, f0=f0)
        # plot_pitch_spectrogram(y=y, times=times, f0=f0)


    except Exception as e:
        error(f"{i} {audio_name}: an error occurred: {e}")
        

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--audio", required=False, help="audio name, youtube id")
    args = vars(ap.parse_args())

    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)

    if 'audio' in args:
        # a single audio file was passed as argument
        calculate_pitch(audio_tuple=(1, args['audio']))

    else:
        # no audio file passed as argument, get file names from config

        compute_pool_size = config.get('compute-pool-size', 2)

        audio_names = config.get('audio-names', [])
        # Use enumerate() to get (index, item) pairs
        indexed_items = enumerate(audio_names)

        # Convert the resulting iterator into a list of tuples
        audio_tuples = list(indexed_items)

        audios_to_process = []
        for i, audio_name in audio_tuples:
            output_csv = csv_path.format(audio_name)
            if os.path.exists(output_csv):
                warn(f"[{output_csv}] exists ... skipping")
            else:
                audios_to_process.append((i, audio_name))

        with multiprocessing.Pool(processes=compute_pool_size) as pool:
            results = pool.map(calculate_pitch, audios_to_process)
