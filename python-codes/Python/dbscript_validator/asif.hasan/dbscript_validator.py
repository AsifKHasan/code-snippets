#!/usr/local/bin/python3

'''
Usage: ./dbscript_validator.py R01_00_00__antarika.sql
'''

import sys
import re
from functional import seq

def list_tables(sqlFile):
    return (seq.open(sqlFile)
        .filter(lambda l: re.search(r'create table[\s]+[A-Za-z0-9_]+', l))
        .map(lambda l: re.sub('create table[\s]+', '', l).strip('\n'))
        )

def main():
    if (len(sys.argv) < 2):
        print('Usage:', sys.argv[0], 'sql-file')
        exit(-1)
    
    sqlFile = sys.argv[1]
    
    print('Parsing file:', sqlFile)
    tables = list_tables(sqlFile)
    print('Tables found:', tables.len())
    print('\n'.join(tables))

if __name__ == '__main__':
    main()
