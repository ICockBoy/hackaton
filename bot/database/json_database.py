import json
import os
from json import JSONDecodeError
from typing import Any


class JSONDATABASE:
    def __init__(self, json_file: str):
        """
        :param json_file: Path to json database file
        """
        self.filedb = json_file.replace("\\", "/")
        if not os.path.isfile(self.filedb):
            if not os.path.exists("/".join(self.filedb.rsplit("/")[:-1])):
                os.makedirs("/".join(self.filedb.rsplit("/")[:-1]))
            self.write({})

    @staticmethod
    def is_jsonable(x):
        try:
            json.loads(x)
            return True
        except JSONDecodeError:
            return False

    def write(self, db_dict: dict):
        with open(self.filedb, "w+") as filedb_stream:
            filedb_stream.write(json.dumps(db_dict, indent=4))

    def read(self):
        with open(self.filedb) as filedb_stream:
            read = filedb_stream.read()
            if self.is_jsonable(read):
                return json.loads(read)
            else:
                return {}

    def save_field(self, field: str, value):
        read = self.read()
        read[field] = value
        self.write(read)

    def get_field(self, field: str):
        read = self.read()
        if field in read:
            return read[field]
        else:
            return None
