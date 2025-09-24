#!/usr/bin/env python

import os
import math
import csv
import argparse
import yaml
import librosa
import librosa.display
import numpy as np
import multiprocessing
from functools import partial

import matplotlib.pyplot as plt
import matplotlib.style as ms

from helper.logger import *
from helper import logger

def calculate_mfcc_from_audio(file_path, n_mfcc=13):
    """
    Calculates MFCCs for audio file.

    Args:
        file_path (str): The path to the M4A audio file.
        n_mfcc (int): The number of MFCCs to compute.

    Returns:
        np.ndarray: A NumPy array containing the MFCCs.
                    Returns None if the file cannot be processed.
    """
    try:
        # Step 1: Load the audio file
        y, sr = librosa.load(file_path, sr=None)
        debug(f"Sampling rate: {sr} Hz")


        # Step 2: Calculate the hop_length for a 20ms interval
        hop_length = int(0.020 * sr)
        debug(f"Calculated hop_length for 20ms: {hop_length} samples")

        # Step 3: Calculate MFCCs
        mfccs = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=n_mfcc,
            hop_length=hop_length
        )

        info(f"Successfully calculated MFCCs for '{file_path}'")
        return y, sr, hop_length, mfccs

    except Exception as e:
        error(f"An error occurred: {e}")
        return None, None, None, None


def save_as_csv(csv_path, data, i):
    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

    debug(f"{i} : data successfully written to {csv_path}")


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
    debug(f"calculating MFCC for {audio_name}")

    # Calculate the first 13 MFCCs
    y, sr, hop_length, mfccs_result = calculate_mfcc_from_audio(audio_file)
    n_frames = mfccs_result.shape[1]
    duration = librosa.get_duration(y=y, sr=sr)
    frame_duration_ms = math.ceil((duration / n_frames) * 1000)
    # Generate a time axis for the plot
    time = np.linspace(0, duration, num=n_frames)

    if mfccs_result is not None:
        debug(f"Shape of the MFCCs array: {mfccs_result.shape}")
        debug(f"Frame duration: {frame_duration_ms}ms")
        # debug("First 5 MFCCs values:\n", mfccs_result[:, :5])

        # from_s = 8.0
        # to_s = 8.5
        # start_row = math.floor((from_s * 1000) / frame_duration_ms)
        # end_row = math.ceil((to_s * 1000) / frame_duration_ms)
        # mfcc_indices = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        # mfccs = mfccs_result[:, start_row:end_row]

        # mfcc_spectrogram(mfccs=mfccs, mfcc_indices=mfcc_indices, sr=sr, hop_length=hop_length)
        # mfcc_line(mfccs=mfccs, mfcc_indices=mfcc_indices, time=time[start_row:end_row])

        save_as_csv(csv_path=csv_path.format(audio_name), data=mfccs_result.T, i=i)


audio_path = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/{}.m4a'
csv_path = '../out/mfcc_data__{}.csv'

if __name__ == "__main__":
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-a", "--audio", required=False, help="audio name, youtube id")
    # ap.add_argument("-t", "--threshold", required=False, help="threshold ration for ENERGY", type=float, default=2.0)
    # args = vars(ap.parse_args())

    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
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
        results = pool.map(calculate_mfcc, audios_to_process)
