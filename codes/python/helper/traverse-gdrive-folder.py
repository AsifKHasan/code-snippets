#!/usr/bin/env python3
''' os.walk() variation with Google Drive API.
'''

import os

from apiclient.discovery import build  # pip install google-api-python-client

FOLDER = 'application/vnd.google-apps.folder'


def get_credentials(scopes, *,
                    secrets='~/client_secret.json',
                    storage='~/storage.json'):
    from oauth2client import file, client, tools

    store = file.Storage(os.path.expanduser(storage))
    creds = store.get()

    if creds is None or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.expanduser(secrets), scopes)
        flags = tools.argparser.parse_args([])
        creds = tools.run_flow(flow, store, flags)
    return creds


creds = get_credentials(scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

service = build('drive', version='v3', credentials=creds)


def iterfiles(name=None, *, is_folder=None, parent=None,
              order_by='folder,name,createdTime'):
    q = []
    if name is not None:
        q.append("name = '{}'".format(name.replace("'", "\\'")))
    if is_folder is not None:
        q.append("mimeType {} '{}'".format('=' if is_folder else '!=', FOLDER))
    if parent is not None:
        q.append("'{}' in parents".format(parent.replace("'", "\\'")))

    params = {'pageToken': None, 'orderBy': order_by}
    if q:
        params['q'] = ' and '.join(q)

    while True:
        response = service.files().list(**params).execute()
        for f in response['files']:
            yield f
        try:
            params['pageToken'] = response['nextPageToken']
        except KeyError:
            return


def walk(top='root', *, by_name: bool = False):
    if by_name:
        top, = iterfiles(name=top, is_folder=True)
    else:
        top = service.files().get(fileId=top).execute()
        if top['mimeType'] != FOLDER:
            raise ValueError(f'not a folder: {top!r}')

    stack = [((top['name'],), top)]
    while stack:
        path, top = stack.pop()

        dirs, files = is_file = [], []
        for f in iterfiles(parent=top['id']):
            is_file[f['mimeType'] != FOLDER].append(f)

        yield path, top, dirs, files

        if dirs:
            stack.extend((path + (d['name'],), d) for d in reversed(dirs))


for kwargs in [{'top': 'SAU-CAS', 'by_name': True}, {}]:
    for path, root, dirs, files in walk(**kwargs):
        print('/'.join(path), f'{len(dirs):d} {len(files):d}', sep='\t')
