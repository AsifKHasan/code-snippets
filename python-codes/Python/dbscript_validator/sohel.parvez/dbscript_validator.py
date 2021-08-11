#!/usr/local/bin/python3

'''
Usage: ./dbscript_validator.py R01_00_00__antarika.sql
'''
import sys
import re

def list_tables(sqlFile):
    return re.findall('create table\s+(.*?)\s+\(', open(sqlFile, 'r').read(), re.DOTALL)

def main():
    if (len(sys.argv) < 2):
        print('Usage:', sys.argv[0], 'sql-file')
        exit(-1)
    
    sqlFile = sys.argv[1]
    names = list_tables(sqlFile)
    print(names)
    print('Total no of tables: '+str(len(names)))
    print('Table names are: \n\t'+'\n\t'.join(names))
    
    
if __name__ == '__main__':
    main()
