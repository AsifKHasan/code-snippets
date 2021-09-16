#!/usr/bin/env python3
'''
usage: ./name-cloud.py --xlsx ./data/names-result.xlsx --outdir ./out/
'''
import json
import os
import shutil
import sys
import time
import datetime
import argparse
import math
import wordcloud
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

class CloudMaker(object):

    def __init__(self, xlsx, outdir):
        self.start_time = int(round(time.time() * 1000))
        s = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d__%H-%M-%S")
        self._XLSX_PATH = xlsx
        self._OUTPUT_DIR = outdir

    def make_cloud(self, df):
        # prepare frequency dict
        df['freq'] = df['freq'].apply(math.log1p).apply(math.ceil)
        df.set_index('name', drop=True, inplace=True)
        d = df.to_dict(orient='dict')['freq']

        # Generate a word cloud image
        namecloud = wordcloud.WordCloud(background_color="white", prefer_horizontal=1.0, colormap="tab10", mode="RGBA").generate_from_frequencies(d)
        #plt.imshow(namecloud, interpolation="bilinear")
        #plt.axis("off")
        #plt.show()
        imgpath = self._OUTPUT_DIR + "{0}.png".format(list(d)[-1])
        namecloud.to_file(imgpath)

    def process_data(self):
        df = self.xl.parse(sheet_name='clusters', skiprows=2, header=None, usecols='B:E', names=['cluster_freq', 'cluster_name', 'member_freq', 'member_name'])

        df.sort_values(['cluster_freq', 'member_freq'], ascending=[0, 0], inplace = True)
        # split into a list of DF - one DF for one cluster
        dl = [g for _, g in df.groupby(['cluster_freq', 'cluster_name'])]
        # some clusters have more frequent members than the cluster frequency, remove them
        dl = list(filter(lambda x: all(x['member_freq'] < x['cluster_freq']), dl))
        # merge cluster and members
        dl = list(map(lambda x: pd.DataFrame({'name': x['member_name'].append(pd.Series(x['cluster_name'].iloc[0])), 'freq' : x['member_freq'].append(pd.Series(x['cluster_freq'].iloc[0]))}), dl))

        # for each df generate the cloud
        for df in dl:
            self.make_cloud(df)

    def generate(self):
        return

    def set_up(self):
        self.xl = pd.ExcelFile(self._XLSX_PATH)

    def tear_down(self):
        self.end_time = int(round(time.time() * 1000))
        print("Script took {} seconds".format((self.end_time - self.start_time)/1000))

    def run(self):
        self.set_up()
        self.process_data()
        self.generate()
        self.tear_down()

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-x", "--xlsx", required=True, help="xlsx file path where the names data is")
    ap.add_argument("-o", "--outdir", required=True, help="output directory where cloud images will be saved")
    args = vars(ap.parse_args())

    maker = CloudMaker(args["xlsx"], args["outdir"])
    maker.run()
