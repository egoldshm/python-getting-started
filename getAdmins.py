from google_spreadsheep_reader import google_spreadsheet_reader
from values_to_bot import SPREADSHEET_ID
from typing import List
RANGE_OF_COMMANDS = 'admins'


def getAdmins() -> List[int]:
    reader = google_spreadsheet_reader(SPREADSHEET_ID, RANGE_OF_COMMANDS)
    values = list(map(lambda i: int(i[0]), reader.values))
    return values