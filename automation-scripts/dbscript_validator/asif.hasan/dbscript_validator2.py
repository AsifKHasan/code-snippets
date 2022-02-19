#!/usr/local/bin/python3

'''
./dbscript_validator2.py /Users/asif.hasan/projects/Celloscope/csb/services/antarika/script/postgres/01-table
'''

import sys
import greptile

if (len(sys.argv) < 2):
    print('Usage:', sys.argv[0], 'rootPath')
    exit(-1)
    
rootDir = sys.argv[1]

files = greptile.grep_rl('create table[ \t]+[A-Z][A-Za-z0-9]+\n', rootDir, '.sql')
for f in files:
    print f
