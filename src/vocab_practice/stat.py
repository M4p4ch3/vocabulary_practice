
from csv import DictReader, DictWriter
import json
from typing import Any, List, Dict

class StatDict():

    KEY_LIST = ["id", "err_nb", "total_nb"]

    class Translation():

        def __init__(self, id: str, err_nb: int = 0, total_nb: int = 0):
            self.id = id
            self.err_nb = err_nb
            self.total_nb = total_nb

        @classmethod
        def from_dict(cls, data_dict: Dict[str, Any]):
            return StatDict.Translation(
                data_dict["id"],
                int(data_dict["err_nb"]),
                int(data_dict["total_nb"]),
            )

        def as_dict(self):
            return {
                "id": self.id,
                "err_nb": self.err_nb,
                "total_nb": self.total_nb,
            }

        def show(self):
            print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))

    def __init__(self, path: str):
        self.path = path
        self.entry_dict: Dict[str, StatDict.Translation] = {}
        self.load()

    def load(self):
        self.entry_dict.clear()
        with open(self.path, "r", encoding="utf8") as csv_file:
            csv_reader = DictReader(csv_file)
            for entry_dict in csv_reader:
                self.entry_dict[entry_dict["id"]] = StatDict.Translation.from_dict(entry_dict)

    def save(self):
        with open(self.path, "w", encoding="utf8") as csv_file:
            csv_writer = DictWriter(csv_file, self.KEY_LIST)
            csv_writer.writeheader()
            for entry in list(self.entry_dict.values()):
                csv_writer.writerow(entry.as_dict())

    def as_dict(self):
        return {
            "entry_list": [entry.as_dict() for entry in list(self.entry_dict.values())]
        }

    def show(self):
        print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))
