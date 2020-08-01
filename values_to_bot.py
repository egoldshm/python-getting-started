from typing import *

from botMenu import BotMenu
from google_spreadsheep_reader import google_spreadsheet_reader

SPREADSHEET_ID = '1ckk82XyjJ7mSxwgDMJYew8dR3AgY8umj1l8XyHVJAIg'
RANGE_OF_COMMANDS = 'range'

file_column = ["name", "type", "father_menu", "answer", "row", "column", "button_inline", "substring"]


def list_to_dict(row):
    result = {}
    for i in range(0, len(row)):
        result[file_column[i]] = row[i]
    for i in range(len(row), len(file_column)):
        result[file_column[i]] = ""
    return result


class data_to_bot:
    def __init__(self):
        self.reset()

    def get_data_from_file(self) -> List[Dict[str, Union[str, Any]]]:
        """
        function that return dict of all the commands in the google spreadsheet

        :return:
        """

        if not self.spreadsheet_reader.values:
            raise Exception("Data not exist in the file with id '{}'".format(SPREADSHEET_ID))

        result = list(filter(lambda item: item["name"] != "", list(map(list_to_dict, self.spreadsheet_reader.values))))

        return result

    def reset(self):
        self.spreadsheet_reader = google_spreadsheet_reader(SPREADSHEET_ID, RANGE_OF_COMMANDS)
        self.botMenu = BotMenu(self.get_data_from_file())
