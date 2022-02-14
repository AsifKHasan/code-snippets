#!/usr/bin/env python3
'''
    generate templated salary enhancement document (letter) from data
'''

import gspread

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.urllib3 import AuthorizedHttp

from pprint import pprint


DATA_CONNECTORS = {
    'Google': {
        'credntial-json': '../conf/credential.json'
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
            {'column': 13, 'key': 'salary'},
            {'column': 14, 'key': 'increment'},
            {'column': 16, 'key': 'effective-from'},
            {'column': 19, 'key': 'designation'},
        ]
    }
}

DATA_SERIALIZERS = {
    'salary-enhancement': {
        'output-dir': '../out/salary-enhancement',
        'output-file': 'salary-enhancement-commands.bat'
    }
}


''' authenticate to data service
    get to Google
'''
def authenticate_to_data_service():
    google_data_connector_spec = DATA_CONNECTORS['Google']

    # get credentials for service-account
    credentials = service_account.Credentials.from_service_account_file(google_data_connector_spec['credntial-json'])
    scoped_credentials = credentials.with_scopes(
                                                [
                                                    "https://spreadsheets.google.com/feeds",
                                                    'https://www.googleapis.com/auth/spreadsheets',
                                                    "https://www.googleapis.com/auth/drive.file",
                                                    "https://www.googleapis.com/auth/drive"
                                                ]
                                            )

    # using gspread for proxying the gsheet API's
    client = gspread.authorize(scoped_credentials)

    # authed_session = AuthorizedSession(credentials)
    # response = authed_session.get('https://www.googleapis.com/storage/v1/b')

    # authed_http = AuthorizedHttp(credentials)
    # response = authed_http.request('GET', 'https://www.googleapis.com/storage/v1/b')

    # wrap the connector in a data-connector object
    data_connector = {'client': client}

    return data_connector


''' acquire data from data source
    get the gsheet and read data
'''
def acquire_data(data_connector):
    gsheet_data_source_spec = DATA_SOURCES['gsheet']

    # get the worksheet where the data is
    gsheet = data_connector['client'].open(title=gsheet_data_source_spec['sheet'])
    ws = gsheet.worksheet(title=gsheet_data_source_spec['worksheet'])

    # get values in the specified range
    values = ws.get_values(gsheet_data_source_spec['data-range'])

    # wrap the data in a source-data object
    source_data = {'data': values}

    return source_data


''' process and transform data
    prepare data in relation to salary enhancement requirement
'''
def process_data(source_data):
    se_data_processor_spec = DATA_PROCESSORS['salary-enhancement']

    raw_data = source_data['data']

    # the data is in a list (rows) of list (columns)
    data = []
    for row in raw_data:
        columns = {}
        if row[20] == 'yes':
            for col_spec in se_data_processor_spec['columns']:
                columns[col_spec['key']] = row[col_spec['column']]

            data.append(columns)

    # wrap the data in a processed-data object
    processed_data = {'data': data}

    return processed_data


''' output data for document generation
    output data for salary enhancement doument generation
'''
def output_data(processed_data):
    se_output_spec = DATA_SERIALIZERS['salary-enhancement']

    data = processed_data['data']

    content = []

    # create the tmp directory
    content.append('if not exist "../../out/salary-enhancement/tmp" mkdir "../../out/salary-enhancement/tmp"')

    content.append('set INPUT_FILE="../../template/salary-enhancement/celloscope__salary-enhancement-template__2022.odt"')
    content.append('')

    # ooo_fieldreplace command line for each data row
    temp_files = []
    for item in data:
        OUTPUT_FILE = f"../../out/salary-enhancement/tmp/celloscope__salary-enhancement__2022__{item['sequence']}.odt"
        temp_files.append(OUTPUT_FILE)

        str = f'python ../../bin/ooo_fieldreplace -i %INPUT_FILE% -o {OUTPUT_FILE} sequence="{item["sequence"]}" name="{item["name"]}" salutation="{item["salutation"]}" salary="{item["salary"]}" increment="{item["increment"]}" designation="{item["designation"]}" effectivefrom="{item["effective-from"]}"'
        content.append(str)

    # ooo_fieldreplace command line for the final odt
    OUTPUT_FILE = f"../../out/salary-enhancement/celloscope__salary-enhancement__2022.odt"
    str = f'python ../../bin/ooo_CAT -o {OUTPUT_FILE} {" ".join(temp_files)}'

    content.append('')
    content.append(str)

    # output file path
    output_path = f"{se_output_spec['output-dir']}/{se_output_spec['output-file']}"
    with open(output_path, 'w') as f:
        print('\n'.join(content), file=f)

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
