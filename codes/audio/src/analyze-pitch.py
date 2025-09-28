#!/usr/bin/env python

# we may need this to get rid of segfault
# conda install -c conda-forge librosa

import os
import sys
import math
# import csv
import argparse
import yaml
import warnings
import pandas as pd
# import soundfile
# from pydub import AudioSegment
import librosa
# import librosa.display
import numpy as np
import multiprocessing
from functools import partial

# import matplotlib.pyplot as plt
# import matplotlib.style as ms

from helper.utils import *
from helper.logger import *
from helper import logger
from pyplot.pitch_plot import *

warnings.filterwarnings('ignore')

audio_path_template = '/home/asifhasan/projects/asif@github.com/code-snippets/automation-scripts/rabindra-shangeet/out/youtube/{}.m4a'
csv_path_template = '../out/csv/pitch/pitch_data__{}.csv'
plot_path_template = '../out/plot/pitch/pitch_{}__{}.svg'

def analyze_pitch(audio_tuple, pitch_plots):
    i, audio_name = audio_tuple
    info(f"{i} {audio_name}: analyzing Pitch from {audio_name}")
    
    csv_path = csv_path_template.format(audio_name)
    debug(f"{i} {audio_name}: loading csv {csv_path}", nesting_level=1)

    df_csv = pd.read_csv(csv_path)
    data = df_csv.to_dict(orient='list')

    debug(f"{i} {audio_name}: csv loaded {csv_path}", nesting_level=1)

    # generate plots
    for pitch_plot in pitch_plots:
        debug(f"plotting: {pitch_plot}", nesting_level=1)
        # some plots need the original voice data
        if pitch_plot in ['spectrogram']:
            audio_file = audio_path_template.format(audio_name)
            debug(f"{i} {audio_name}: audio data required for {pitch_plot} .. loading {audio_name}", nesting_level=2)
            try:
                # Step 1: Load the audio file
                y, sr = librosa.load(audio_file)
                debug(f"{i} {audio_name}: audio data required for {pitch_plot} .. loaded  {audio_name}", nesting_level=2)

            except Exception as e:
                error(f"{i} {audio_name}: an error occurred: {e}")
                continue

        times = data['time']
        f0 = data['f0']
        if pitch_plot == 'frequency':
            plot = plot_pitch_frequency(times=times, f0=f0)

        if pitch_plot == 'spectrogram':
            plot = plot_pitch_spectrogram(y=y, times=times, f0=f0)

        if pitch_plot == 'contour':
            plot = plot_pitch_contour(times=times, f0=f0)

        plot_path = plot_path_template.format(pitch_plot, audio_name)
        plot.savefig(plot_path, format='svg')
        info(f"{i} {audio_name}: {pitch_plot} saved at {plot_path}", nesting_level=1)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--audio", required=False, help="audio name, youtube id", default=argparse.SUPPRESS)
    args = vars(ap.parse_args())

    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
    pitch_plots = config.get('pitch_plots', [])

    if 'audio' in args:
        # a single audio file was passed as argument
        analyze_pitch(audio_tuple=(1, args['audio']), pitch_plots=pitch_plots)

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

        process_partial = partial(analyze_pitch, pitch_plots=pitch_plots)
        with multiprocessing.Pool(processes=compute_pool_size) as pool:
            results = pool.map(process_partial, audios_to_process)

