from datetime import datetime
from typing import Callable

from helpers.Watcher import Watcher
from helpers.logging import setup_logging, main_logger as logger
from helpers.utils import get_sheet, datetime_to_excel_date

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1ZsVdYrz2bb9E8DJgm04nmR-8Dv6_6JTdb1ixIOomPTU'

CONTENT_KEY_TEXT = 'END OF TRANSACTION REPORT'
EXCLUDED_VALUES = ['USD', '%']

sheet = get_sheet(SERVICE_ACCOUNT_FILE, SCOPES)


def make_on_modified(rng: str, columns: list[str]) -> Callable[[str], None]:
    def on_modified(content: str):
        if CONTENT_KEY_TEXT not in content:
            return
        output = []
        for text in content.split('\n'):
            try:
                key, val = text.split(': ')
            except ValueError:
                continue
            if key.strip() in columns:
                for i in EXCLUDED_VALUES:
                    val = val.replace(i, '')
                output.append(val.strip())
        excel_date = datetime_to_excel_date(datetime.now())
        output.insert(0, excel_date)
        logger.info(output)
        sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=rng, valueInputOption='USER_ENTERED',
                              body={'values': [output]}).execute()

    return on_modified


WATCH_FILES = {
    '/logs/DoraBot1.log': make_on_modified('Sheet1!A2',
                                           ['cumulative pnl', 'overall fund', 'overall pnl(%)', 'total losing trade',
                                            'total completed trade', 'active trade', 'leverage']),
    '/logs/degen-dora.log': make_on_modified('Sheet2!A2',
                                             ['cumulative pnl', 'overall fund', 'overall pnl(%)',
                                              'total completed trade', 'total losing trade', 'total losing usdt',
                                              'total losing (%)', 'active trade', 'leverage']),
}


def main():
    setup_logging()
    watcher = Watcher(WATCH_FILES)
    watcher.run()


if __name__ == '__main__':
    main()
