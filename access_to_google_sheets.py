from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from httplib2 import Http

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1uR5PNgxpaFc2331W6wXrwIY_Zi-F3gvNZmUIA4vXLuE'
RANGE_OF_COMMANDS = 'range'

file_column = ["name", "is_menu", "father_menu", "answer", "row", "column", "button_inline"]
def get_dict_from_list(row):
    result = {}
    for i in range(0, len(row)):
        result[file_column[i]] = row[i]
    for i in range(len(row), len(file_column)):
        result[file_column[i]] = ""
    return result


def get_data_from_file():
    creds = None
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path_of_token = os.path.join(THIS_FOLDER, 'token.pickle')
    if os.path.exists(path_of_token):
        with open(path_of_token, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            path_of_credentials = os.path.join(THIS_FOLDER, "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(path_of_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=RANGE_OF_COMMANDS).execute()
    values = result.get('values', [])

    if not values:
        return None
    result = []
    for i in values:
        result.append(get_dict_from_list(i))
    return result


if __name__ == '__main__':
    print(get_data_from_file())
