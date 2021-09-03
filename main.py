from helpers.Watcher import Watcher
from helpers.logging import setup_logging, main_logger as logger
from helpers.utils import get_sheet

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1ZsVdYrz2bb9E8DJgm04nmR-8Dv6_6JTdb1ixIOomPTU'

CONTENT_KEY_TEXT = 'END OF TRANSACTION REPORT'
CONTENT_COLUMNS = ['cumulative pnl', 'overall fund', 'overall pnl(%)', 'total losing trade', 'total completed trade',
                   'active trade', 'leverage']
EXCLUDED_VALUES = ['USD', '%']

sheet = get_sheet(SERVICE_ACCOUNT_FILE, SCOPES)


def on_modified(content: str):
    if CONTENT_KEY_TEXT not in content:
        return
    output = []
    for text in content.split('\n'):
        try:
            key, val = text.split(': ')
        except ValueError:
            continue
        if key.strip() in CONTENT_COLUMNS:
            for i in EXCLUDED_VALUES:
                val = val.replace(i, '')
            output.append(val.strip())
    logger.info(output)
    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A2', valueInputOption='USER_ENTERED',
                          body={'values': [output]}).execute()


WATCH_FILES = {'/logs/DoraBot1.log': on_modified}


def main():
    setup_logging()
    watcher = Watcher(WATCH_FILES)
    watcher.run()


if __name__ == '__main__':
    main()
