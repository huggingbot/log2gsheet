import io
import os
from datetime import datetime
from os.path import join, abspath, exists
from typing import List

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


def build_path(paths: List[str], use_cwd=False, with_filename=True) -> str:
    filename = None
    if with_filename:
        filename = paths.pop()
    if use_cwd:
        directory = join(*paths)
    else:
        directory = join(root_dir(), *paths)
    if not exists(directory):
        os.makedirs(directory)
    return join(directory, filename) if with_filename else directory


def root_dir():
    return abspath(os.sep)


def datetime_to_excel_date(date1) -> float:
    """
    It appears that the Excel "serial date" format is actually the number of days since 1900-01-00, with a fractional
    component that's a fraction of a day, based on http://www.cpearson.com/excel/datetime.htm. (I guess that date
    should actually be considered 1899-12-31, since there's no such thing as a 0th day of a month)
    """
    temp = datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)
