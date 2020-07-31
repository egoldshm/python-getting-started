import os
from typing import List, Any


class save_data_in_file:
    data: List[str]

    def __init__(self, file_name):
        self.data = []
        self.file_name = file_name
        if not os.path.isfile(file_name):
            file = open(file_name, "w")
            file.close()
        else:
            file = open(file_name, "r")
            self.data = file.readlines()

    def name_exist(self, name: str) -> bool:
        return name in self.data

    def add_name(self, name: str):
        pass
