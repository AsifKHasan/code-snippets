#!/usr/bin/env python

# we may need this to get rid of segfault
# conda install -c conda-forge librosa

import os
import sys
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
csv_path = '../out/csv/amplitude-envelope/amplitude-envelope__{}.csv'
frame_duration_s = 0.020

def plot_rms_energy(signal, rmse1, rmse2, frame_length, hop_length):
    frames = range(0, rmse1.size)
    t = librosa.frames_to_time(frames, hop_length=hop_length)

    fig = plt.figure(figsize=(12, 6))
    librosa.display.waveshow(signal, alpha=0.5)
    plt.plot(t, rmse1, color='r')
    plt.plot(t, rmse2, color='y')
    plt.ylim(-1, 1)
    plt.title('RMS Energy')

    plt.show()

def calculate_rmse(y, frame_length, hop_length):
    rms = []

    for i in range(0, len(y), hop_length):
        rms_this_frame = np.sqrt(np.sum(y[i:i+frame_length]**2) / frame_length)
        rms.append(rms_this_frame)

    return np.array(rms)



def calculate_rms_energy(audio_tuple):
    i, audio_name = audio_tuple
    audio_file = audio_path.format(audio_name)
    info(f"{i} {audio_name}: calculating RMS Energy")

    try:
        # Step 1: Load the audio file
        y, sr = librosa.load(audio_file)
        debug(f"{i} {audio_name}: sampling rate: {sr} Hz", nesting_level=1)
        debug(f"{i} {audio_name}: frame duration: {frame_duration_s * 1000}ms", nesting_level=1)

        # plot_amplitude(signal=y)

        # calculate rmse
        frame_length = int(sr * frame_duration_s)
        debug(f"{i} {audio_name}: frame length: {frame_length}", nesting_level=1)

        hop_length = int(frame_duration_s * sr / 2)
        debug(f"{i} {audio_name}: hop length for 20ms: {hop_length} samples", nesting_level=1)

        rms_energy1 = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        rms_energy2 = calculate_rmse(y=y, frame_length=frame_length, hop_length=hop_length)

        plot_rms_energy(signal=y, rmse1=rms_energy1, rmse2=rms_energy2, frame_length=frame_length, hop_length=hop_length)

        info(f"{i} {audio_name}: successfully calculated RMS Energy")

    except Exception as e:
        error(f"{i} {audio_name}: an error occurred: {e}")
        sys.exit(-1)
        

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--audio", required=False, help="audio name, youtube id", default=argparse.SUPPRESS)
    args = vars(ap.parse_args())

    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)

    if 'audio' in args:
        # a single audio file was passed as argument
        calculate_rms_energy(audio_tuple=(1, args['audio']))

    else:
        # no audio file passed as argument, get file names from config

        compute_pool_size = config.get('compute-pool-size', 2)

        audio_names = config.get('audio_names', [])
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
            results = pool.map(calculate_rms_energy, audios_to_process)
