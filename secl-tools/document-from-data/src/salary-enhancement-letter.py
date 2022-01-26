#!/usr/bin/env python3
'''
    generate templated salary enhancement document (letter) from data
'''

DATA_CONNECTORS = {
    'Google': {
        credntial_json: '../conf/credential.json'
    }
}

DATA_SOURCES = {
    'gsheet': {
        'sheet': 'spectrum__salary-revision__2022',
        'worksheet': 'spectrum-2022',
        'start_row': 4
    }
}


DATA_PROCESSORS = {
    'salary-enhancement': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'name'},
            {'column': 2, 'key': 'salutation'},
            {'column': 3, 'key': 'wing'},
            {'column': 4, 'key': 'unit'},
            {'column': 5, 'key': 'supervisor'},
            {'column': 6, 'key': 'stage'},
            {'column': 11, 'key': 'salary'},
            {'column': 12, 'key': 'increment'},
            {'column': 16, 'key': 'promotion'},
            {'column': 17, 'key': 'grade'},
            {'column': 18, 'key': 'designation'},
        ]
    }
}



''' authenticate to data service
    get to Google
'''
def authenticate_to_data_service():



''' acquire data from data source
    get the gsheet and read data
'''
def acquire_data():



''' process and transform data
    prepare data in relation to salary enhancement requirement
'''
def process_data():




if __name__ == '__main__':
    data_connector = authenticate_to_data_service()
