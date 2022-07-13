#!/usr/bin/env python3

import re


'''split text into lines and remove spaces and any special character from the begining
'''
def split_and_dress(value):
    lines = value.split('\n')
    regex = r'^[-\s•]+'
    lines = [re.sub(regex, '', s) for s in lines]
    regex = r'[\s]+$'
    lines = [re.sub(regex, '', s) for s in lines]

    return lines
