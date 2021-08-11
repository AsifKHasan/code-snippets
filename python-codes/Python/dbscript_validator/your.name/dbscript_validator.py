#!/usr/local/bin/python3

'''
Usage: ./dbscript_validator.py R01_00_00__antarika.sql
'''

def list_tables(sqlFile):
    # ...........

def main():
    if (len(sys.argv) < 2):
        print('Usage:', sys.argv[0], 'sql-file')
        exit(-1)
    
    sqlFile = sys.argv[1]
    
    # ............
    
if __name__ == '__main__':
    main()