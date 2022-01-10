#!/usr/bin/env python3
'''
from command line
------------------
./bangla-word-generator.py --data './data/bangla-words.txt' --outdir './output' --startswith 'অ'

from py files
------------------
'''

import argparse
import datetime
import time
import json
import re
import os

patterns = [
    {
        "search-for": "[ ]*\[.+\][ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[ ]*\(.+\)[ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[, ]*কি০[ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[, ]*তু০[ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[, ]*দ্র০[ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[, ]*যে০[ ]*",
        "replace-with": " "
    },
    {
        "search-for": "[,.;:?‘'’]\n",
        "replace-with": "\n"
    },
    {
        "search-for": "[‘'’]",
        "replace-with": ""
    },
    {
        "search-for": " [ ]+",
        "replace-with": " "
    },
    {
        "search-for": "[ ]+\n",
        "replace-with": "\n"
    },
    {
        "search-for": "\n[ ]+",
        "replace-with": "\n"
    },
    {
        "search-for": "\n[\n]+",
        "replace-with": "\n"
    },
    {
        "search-for": "\n,",
        "replace-with": ","
    },
    {
        "search-for": " ,",
        "replace-with": ","
    }
]

class WordGenerator(object):

    def __init__(self, datafile, outdir, startswith):
        self._start_time = int(round(time.time() * 1000))
        self._DATA_FILE = datafile
        self._OUTPUT_DIR = outdir
        self._STARTSWITH = startswith
        self._START_LIST = startswith.split(',')

        # output file name
        f_name, f_ext = os.path.splitext(self._DATA_FILE)
        f_name = os.path.basename(f_name)
        self._output_file_path = '{}/{}-{}.{}'.format(self._OUTPUT_DIR, f_name, self._STARTSWITH, f_ext)

    def run(self):
        self.set_up()
        self.read_data()
        self.generate_words()
        self.tear_down()

    def set_up(self):
        pass

    def read_data(self):
        with open(self._DATA_FILE, "r") as f:
            self._INPUT = f.read()

    def generate_words(self):
        # apply RE patterns for sub
        lines = self._INPUT
        for p in patterns:
            lines = re.sub(p["search-for"], p["replace-with"], lines)
            #lines = re.sub(p["search-for"], p["replace-with"], lines, flags=re.DOTALL)

        lines = lines.split('\n')
        lines_comma = list(filter(lambda line: ',' in line, lines))
        lines_words = list(filter(lambda line: ',' not in line, lines))

        self._OUTPUT = lines_words

    def tear_down(self):
        if not isinstance(self._OUTPUT, str):
            self._OUTPUT = '\n'.join(self._OUTPUT)

        with open(self._output_file_path, "w") as f:
            f.write(self._OUTPUT)

        self._end_time = int(round(time.time() * 1000))
        print("Script took {} seconds".format((self._end_time - self._start_time)/1000))

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--datafile", required=True, help="data file where the raw list is")
    ap.add_argument("-o", "--outdir", required=True, help="output directory where output word list will be stored")
    ap.add_argument("-s", "--startswith", required=True, help="list of char/word as the begining sequence for words to be extracted")
    args = vars(ap.parse_args())

    processor = WordGenerator(args["datafile"], args["outdir"], args["startswith"])
    processor.run()
