#!/usr/bin/env python

# we may need this to get rid of segfault
# conda install -c conda-forge librosa

import os
import sys
import math
import warnings
import numpy as np

import librosa
# import librosa.display

import matplotlib.pyplot as plt
import matplotlib.style as ms

from helper.utils import *
from helper.logger import *
from helper import logger

warnings.filterwarnings('ignore')

def plot_pitch_frequency(times, f0):
    # we have time in 0.02 seconds, make one second to span two inches in x-axis
    x_size = len(times) * 0.04
    fig, ax = plt.subplots(figsize=(x_size, 5))

    # plot the F0
    ax.plot(times, f0, label='F0', color='blue', linewidth=1)

    # Generate tick positions: [0.0, 0.1, 0.2, 0.3, ..., max_time]
    tick_interval = 0.1
    max_time = times[-1]
    x_ticks = np.arange(0, max_time + tick_interval, tick_interval)
    locs, labels = plt.xticks(x_ticks,
        rotation=45, 
        ha='right'
    )

    # 2. Iterate through the ticks and labels to customize the full second labels
    default_fontsize = 6
    large_fontsize = 10

    for numeric_loc, label_object in zip(x_ticks, labels):
        # Check if the tick location is a whole number (a full second)
        if np.isclose(numeric_loc % 1.0, 0.0):
            # Customize for full second
            label_object.set_fontsize(large_fontsize)
            label_object.set_fontweight('bold')
        else:
            # Set default size for other labels
            label_object.set_fontsize(default_fontsize)
            label_object.set_fontweight('normal')

    # Add Context: Highlight the typical adult F0 range
    plt.axhspan(85, 255, facecolor='gray', alpha=0.1, label='Typical Adult F0 Range')

    plt.ylim(0, 500)

    # Set the plot labels and title
    ax.set_title('F0 Contour')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Add a grid for easier reading
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Display the plot
    plt.tight_layout()

    # plt.show()
    return plt


def plot_pitch_spectrogram(y, times, f0):
    fig, ax = plt.subplots(figsize=(20, 12))

    # Plot the spectrogram
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')

    # Plot the F0 contour on top of the spectrogram
    ax.plot(times, f0, label='F0 (PYIN)', color='cyan', linewidth=3)

    ax.set(title='Pitch (F0) analysis with PYIN', xlabel='Time (s)', ylabel='Frequency (Hz)')
    ax.legend(loc='upper right')

    # plt.show()
    return plt
