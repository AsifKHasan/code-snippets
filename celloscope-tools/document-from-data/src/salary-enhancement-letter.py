#!/usr/bin/env python3
'''
    generate templated salary enhancement document (letter) from data
'''

import os
from pprint import pprint

from helper.google.google_helper import *
from helper.openoffice.odt.odt_helper import *
from helper.logger import *

DATA_CONNECTORS = {
    'Google': {
        'credential-json': '../conf/credential.json'
    }
}

DATA_SOURCES = {
    'gsheet': {
        'sheet': 'celloscope__salary-revision__2022',
        'worksheet': 'celloscope-2022',
        'start_row': 4,
        'data-range': 'A5:U'
    }
}

DATA_PROCESSORS = {
    'salary-enhancement': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 7, 'key': 'designation'},
            {'column': 16, 'key': 'salary'},
            {'column': 17, 'key': 'increment'},
            {'column': 19, 'key': 'effective-from'},
        ]
    }
}

DATA_SERIALIZERS = {
    'salary-enhancement': {
        'input-template': '../template/salary-enhancement/celloscope__salary-enhancement-template__2022.odt',
        'output-dir': '../out/salary-enhancement',
        'output-file-pattern': 'celloscope__salary-enhancement__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'celloscope__salary-enhancement__2022.odt',
        'pdf-output-for-merged-file': True,
    }
}


''' authenticate to data service
    get to Google
'''
def authenticate_to_data_service():
    google_data_connector_spec = DATA_CONNECTORS['Google']

    debug('authenticating with Google')
    client = connector_client(google_data_connector_spec)
    debug('authenticating with Google ... done')

    # wrap the connector in a data-connector object
    data_connector = {'client': client}

    return data_connector


''' acquire data from data source
    get the gsheet and read data
'''
def acquire_data(data_connector):
    gsheet_data_source_spec = DATA_SOURCES['gsheet']

    debug('acquiring data')
    values = gsheet_data(data_connector['client'], gsheet_data_source_spec)
    debug('acquiring data ... done')

    # wrap the data in a source-data object
    source_data = {'data': values}

    return source_data


''' process and transform data
    prepare data in relation to salary enhancement requirement
'''
def process_data(source_data):
    se_data_processor_spec = DATA_PROCESSORS['salary-enhancement']

    raw_data = source_data['data']

    debug('processing data')
    # the data is in a list (rows) of list (columns)
    data = []
    for row in raw_data:
        columns = {}
        if row[20] == 'yes':
            for col_spec in se_data_processor_spec['columns']:
                columns[col_spec['key']] = row[col_spec['column']]

            data.append(columns)

    debug('processing data ... done')

    # wrap the data in a processed-data object
    processed_data = {'data': data}

    return processed_data


''' output data for document generation
    output data for salary enhancement doument generation
'''
def output_data(processed_data):
    se_output_spec = DATA_SERIALIZERS['salary-enhancement']

    data = processed_data['data']
    tmp_dir = se_output_spec['output-dir'] + '/tmp'

    # crete directories in case they do not exist
    os.makedirs(tmp_dir, exist_ok=True)

    debug('generating output')

    # generate files for each data row
    temp_files = []
    for item in data:
        temp_file_path = tmp_dir + '/' + se_output_spec['output-file-pattern'].format(item['sequence'], item['name'].lower().replace(' ', '-'))
        temp_files.append(temp_file_path)

        debug(f'.. generating odt for {item["name"]}')
        # generate the file
        fields = {"sequence": item["sequence"], "name": item["name"], "salutation": item["salutation"], "salary": item["salary"], "increment": item["increment"], "designation": item["designation"], "effectivefrom": item["effective-from"]}
        replace_fields(se_output_spec['input-template'], temp_file_path, fields)
        debug(f'.. generating odt for {item["name"]} ... done')

        # generate pdf if instructed to do so
        if se_output_spec['pdf-output-for-files']:
            debug(f'.. generating pdf from {temp_file_path}')
            generate_pdf(temp_file_path, tmp_dir)
            debug(f'.. generating pdf from {temp_file_path} ... done')

    # merge files if instructed to do so
    if se_output_spec['merge-files']:
        output_file_path = se_output_spec['output-dir'] + '/' + se_output_spec['merged-file-pattern'].format()
        debug('merging odt files')
        merge_files(temp_files, output_file_path)
        debug('merging odt files ... done')

    # generate pdf if instructed to do so
    if se_output_spec['pdf-output-for-merged-file']:
        debug('generating pdf from merged odt')
        generate_pdf(output_file_path, se_output_spec["output-dir"])
        debug('generating pdf from merged odt ... done')

    debug('generating output ... done')

    return


if __name__ == '__main__':
    # get the appropriate data-connector
    data_connector = authenticate_to_data_service()

    # get raw data from source
    source_data = acquire_data(data_connector)

    # get processed data from the raw data
    processed_data = process_data(source_data)

    # serialize final output from data
    output_data(processed_data)
