import io

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_file_content_from_byte_position(file_path, position):
    with open(file_path, 'rb+') as f:
        f.seek(position)
        return f.read().decode('utf-8')


def get_file_last_byte_position(file_path):
    with open(file_path, 'rb+') as f:
        f.seek(0, io.SEEK_END)
        return f.tell()


def get_sheet(svc_acc_file, scopes):
    creds = service_account.Credentials.from_service_account_file(svc_acc_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    return sheet
