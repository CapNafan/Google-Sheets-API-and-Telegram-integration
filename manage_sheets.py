import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'credentials.json'   # this json is created in google service account
spreadsheet_id = '1ApmXsn_QfVVIozsHrLNEozPuYzefp9bnH4ife1BINms'  # id following https://docs.google.com/spreadsheets/d/

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',  # choosing which scopes we are going to work with
        'https://www.googleapis.com/auth/drive'
    ])

# The modified http.request method will add authentication headers to each request
http_auth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=http_auth)  # Construct a Resource object for interacting with an API


def get_data_from_sheets():

    rows = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:D',
        majorDimension='ROWS'
    ).execute()['values'][1:]

    for row in rows:    # if dollar cell is empty it's set to 0
        if row[2] == '':
            row[2] = 0

    rows = [list(map(int, row[:3])) + [row[3]] for row in rows]
    return rows
