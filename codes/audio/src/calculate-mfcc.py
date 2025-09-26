#!/usr/bin/env python

import os
import math
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
csv_path = '../out/csv/mfcc/mfcc_data__{}.csv'
frame_duration_s = 0.020
n_mfcc = 13

def mfcc_line(mfccs, mfcc_indices, time):
    # Define colors for the plots
    colors = plt.get_cmap('viridis', len(mfcc_indices))

    # Create the plot
    plt.figure(figsize=(12, 6))
    
    for i, mfcc_index in enumerate(mfcc_indices):
        # Extract the desired MFCC coefficient and plot it
        single_mfcc = mfccs[mfcc_index, :]
        plt.plot(time, single_mfcc, color=colors(i), label=f'MFCC {mfcc_index}')

    plt.title('Multiple MFCC Coefficients vs. Time')
    plt.xlabel('Time (s)')
    plt.ylabel('MFCC Value')
    plt.grid(True)
    plt.legend()
    plt.show()


def mfcc_spectrogram(mfccs, mfcc_indices, sr, hop_length):
    # Visualize the MFCCs
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(mfccs[mfcc_indices, :], sr=sr, x_axis='time', hop_length=hop_length)
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()


def calculate_mfcc(audio_tuple):
    i, audio_name = audio_tuple
    audio_file = audio_path.format(audio_name)

    # Calculate the first 13 MFCCs
    info(f"{i} {audio_name}: calculating MFCC")
    debug(f"{i} {audio_name}: frame duration: {frame_duration_s * 1000}ms", nesting_level=1)
    try:
        # Step 1: Load the audio file
        y, sr = librosa.load(audio_file)
        debug(f"{i} {audio_name}: sampling rate: {sr} Hz", nesting_level=1)

        # Step 2: Calculate the hop_length for a 20ms interval
        hop_length = int(frame_duration_s * sr)
        debug(f"{i} {audio_name}: calculated hop_length for 20ms: {hop_length} samples", nesting_level=1)

        # Step 3: Calculate MFCCs
        mfccs = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=n_mfcc,
            hop_length=hop_length
        )


    except Exception as e:
        error(f"{i} {audio_name}: an error occurred: {e}")
        return

    n_frames = mfccs.shape[1]
    duration = librosa.get_duration(y=y, sr=sr)

    # Generate a time axis for the plot
    time = librosa.frames_to_time(np.arange(n_frames), sr=sr, hop_length=hop_length)
    # time = np.linspace(0, duration, num=n_frames)
    # print(time.T)

    # append the mfcc to the time series
    mfccs = np.append([time], mfccs, axis=0)

    if mfccs is not None:
        debug(f"{i} {audio_name}: shape of the MFCCs array: {mfccs.shape}", nesting_level=1)
        # debug("First 5 MFCCs values:\n", mfccs_result[:, :5])
        info(f"{i} {audio_name}: successfully calculated MFCCs")

        # from_s = 8.0
        # to_s = 8.5
        # start_row = math.floor((from_s * 1000) / frame_duration_ms)
        # end_row = math.ceil((to_s * 1000) / frame_duration_ms)
        # mfcc_indices = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        # mfccs = mfccs[:, start_row:end_row]

        # mfcc_spectrogram(mfccs=mfccs, mfcc_indices=mfcc_indices, sr=sr, hop_length=hop_length)
        # mfcc_line(mfccs=mfccs, mfcc_indices=mfcc_indices, time=time[start_row:end_row])

        column_names = ['seconds', 'MFCC_00', 'MFCC_01', 'MFCC_02', 'MFCC_03', 'MFCC_04', 'MFCC_05', 'MFCC_06', 'MFCC_07', 'MFCC_08', 'MFCC_09', 'MFCC_10', 'MFCC_11', 'MFCC_12']
        save_as_csv(csv_path=csv_path.format(audio_name), data=mfccs.T, column_names=column_names)
        info(f"{i} {audio_name}: data successfully written to {csv_path.format(audio_name)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--audio", required=False, help="audio name, youtube id", default=argparse.SUPPRESS)
    args = vars(ap.parse_args())

    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)

    if 'audio' in args:
        # a single audio file was passed as argument
        calculate_mfcc(audio_tuple=(1, args['audio']))

    else:
        # no audio file passed as argument, get file names from config
        compute_pool_size = config.get('compute-pool-size', 2)

        audio_names = config.get('audio_names', [])
        info(f"processing {len(audio_names)} audio files")

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
            results = pool.map(calculate_mfcc, audios_to_process)
