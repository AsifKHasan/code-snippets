#!/usr/bin/env python

import os
import json
import yaml
import argparse
import requests
import multiprocessing
from bs4 import BeautifulSoup
from functools import partial
from pathlib import Path

from helper.logger import *
from helper import logger

def song_from_url(data, attributes):
    try:
        response = requests.get(data['url'])
        response.raise_for_status()

        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        
        # Find the specific <td> element
        # The .find() method returns the first matching element it finds
        td_element = soup.find('td', attributes)

        if td_element:
            # the td may have <p>, discard those
            paragraph_to_discard = td_element.find('p')
            if paragraph_to_discard:
                paragraph_to_discard.extract()

            # Return the text content of the element
            data['lyric'] = td_element.get_text(separator='\n', strip=False).strip()
            # print(lyric)
            return data
        else:
            return data
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return data


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    args = vars(ap.parse_args())

    # read config.yml
    config_path = '../conf/config.yml'
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    config_path = Path(config_path).resolve()
    logger.LOG_LEVEL = config.get('log-level', 0)
    output_dir = config.get('output-dir')
    output_path = Path(output_dir).resolve()
    extract_pool_size = config.get('extract-pool-size', 2)

    url_list = config.get('links-to-open', [])
    url_list = [{'id': str(n), 'url': f"http://www.gitabitan.net/top.asp?songid={n}"} for n in url_list]

    attributes = {'id': ' ccelltd1'}
    # attributes = {'class': 'ur10'}
    process_partial = partial(song_from_url, attributes=attributes)
    with multiprocessing.Pool(processes=extract_pool_size) as pool:
        # Use pool.map to apply the worker_function to each item
        results = pool.map(process_partial, url_list[:4])

    output_file = f"{output_path}/song-lyrics.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for song in results:
            # print(song)
            f.write(song['id'])
            f.write('\n')
            f.write(song['lyric'])
            f.write('\n')
            f.write('\n')
