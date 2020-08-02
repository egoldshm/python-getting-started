import datetime
import os
from typing import List


class Report_to_file:
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.isfile(file_name):
            file = open(file_name, "w")
            file.close()

    def addLine(self, *line: str):
        file = open(self.file_name, "a")
        line = map(str, line)
        file.write("\n{0},{1}".format(datetime.datetime.now(), ",".join(line)))
        file.close()
