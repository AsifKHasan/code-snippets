#!/usr/bin/env python3

import gspread

from googleapiclient.discovery import build
from google.oauth2 import service_account

''' Google service wrapper
'''
class GoogleService(object):

    ''' constructor
    '''
    def __init__(self, service_account_json_path):

        # get credentials for service-account
        credentials = service_account.Credentials.from_service_account_file(service_account_json_path)
        scoped_credentials = credentials.with_scopes(
                                                    [
                                                        "https://spreadsheets.google.com/feeds",
                                                        'https://www.googleapis.com/auth/spreadsheets',
                                                        "https://www.googleapis.com/auth/drive.file",
                                                        "https://www.googleapis.com/auth/drive"
                                                    ]
                                                )

        # the gsheet service
        self.gsheet_service = build('sheets', 'v4', credentials=credentials)

        # the drive service
        self.drive_service = build('drive', 'v3', credentials=credentials)

        # using gspread for proxying the gsheet API's
        self.gspread = gspread.authorize(scoped_credentials)

        # authed_session = AuthorizedSession(credentials)
        # response = authed_session.get('https://www.googleapis.com/storage/v1/b')

        # authed_http = AuthorizedHttp(credentials)
        # response = authed_http.request('GET', 'https://www.googleapis.com/storage/v1/b')
