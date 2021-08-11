#!/usr/local/bin/python3

'''
Usage: ./dbscript_validator.py R01_00_00__antarika.sql
'''

import sys
import re

def list_tables(sqlFile):
    tableNames=[]
    try:
        sqlf=open(sqlFile)
        texts=sqlf.read()

        tableNames=re.findall('create\s+table\s+([a-zA-z0-9_]+)\s*\(', texts, flags=re.IGNORECASE)

        sqlf.close()
        return tableNames

    except IOError:
        return

def main():
    if (len(sys.argv) < 2):
        print("Usage: " + sys.argv[0] + " sql-file")
        exit(-1)

    sqlFile = sys.argv[1]
    print("Parsing file: " + sqlFile)
    tableNames = list_tables(sqlFile)

    if tableNames is None:
        print("file can not be read")
        exit(-2)

    if len(tableNames) == 0:
        print('No table found')
    else:
        print('Total table :', len(tableNames))
        print('Table Names :\n', '\n'.join(tableNames))

if __name__ == '__main__':
    main()

