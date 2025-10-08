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

def plot_amplitude_envelope(signal, ae, frame_length, hop_length):
    frames = range(0, ae.size)
    t = librosa.frames_to_time(frames, hop_length=hop_length)

    fig = plt.figure(figsize=(12, 6))
    # librosa.display.waveshow(signal, alpha=0.5)
    plt.plot(t, ae, color='r')
    plt.ylim(-1, 1)
    plt.title('Amplitude Envelope')

    plt.show()

def plot_amplitude(signal):
    fig = plt.figure(figsize=(12, 6))
    librosa.display.waveshow(signal, alpha=0.6)
    plt.ylim(-1, 1)
    plt.title('Amplitude Envelope')

    plt.show()


def calculate_ae(audio_tuple):
    i, audio_name = audio_tuple
    audio_file = audio_path.format(audio_name)
    info(f"{i} {audio_name}: calculating Amplitude Envelope")

    try:
        # Step 1: Load the audio file
        y, sr = librosa.load(audio_file)
        debug(f"{i} {audio_name}: sampling rate: {sr} Hz", nesting_level=1)
        debug(f"{i} {audio_name}: frame duration: {frame_duration_s * 1000}ms", nesting_level=1)

        # plot_amplitude(signal=y)

        # calculate envelope
        frame_length = int(sr * frame_duration_s) 
        debug(f"{i} {audio_name}: frame length: {frame_length}", nesting_level=1)

        hop_length = int(frame_duration_s * sr / 2)
        debug(f"{i} {audio_name}: hop length for 20ms: {hop_length} samples", nesting_level=1)

        amplitude_envelope = []
        # iterate over each frame
        for i in range(0, len(y), hop_length):
            this_frame_amplitude_envelope = max(y[i:i+hop_length])
            amplitude_envelope.append(this_frame_amplitude_envelope)

        plot_amplitude_envelope(signal=y, ae=np.array(amplitude_envelope), frame_length=frame_length, hop_length=hop_length)

        info(f"{i} {audio_name}: successfully calculated Amplitude Envelope")

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
        calculate_ae(audio_tuple=(1, args['audio']))

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
            results = pool.map(calculate_ae, audios_to_process)
