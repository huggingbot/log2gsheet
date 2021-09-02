import io
import os
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
