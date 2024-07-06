
"""
English vocabulary trainer
"""

from argparse import ArgumentParser
from csv import DictReader, DictWriter
from enum import Enum
import json
import random
from typing import Any, List

QUESTION_NB_DFLT = 5

class Dict():

    class Translation():

        class Destination():

            def __init__(self, short: str, long: str = ""):
                self.short = short
                self.long = long
                self.example_list: List[str] = []

            @classmethod
            def from_dict(cls, data_dict: dict[str, Any]):
                entry = cls(data_dict["short"])
                if "long" in data_dict:
                    entry.long = data_dict["long"]
                if "example_list" in data_dict:
                    for example in data_dict["example_list"]:
                        entry.example_list += [example]
                return entry

            def as_dict(self):
                data_dict: dict[str, Any] = {
                    "short": self.short
                }
                if self.long:
                    data_dict["long"] = self.long
                if len(self.example_list) > 0:
                    data_dict["example_list"] = [example for example in self.example_list]
                return data_dict

        def __init__(self, id: str, type: str, dst: Destination):
            self.id = id
            self.type = type
            self.dst = dst

        @classmethod
        def from_dict(cls, data_dict: dict):
            dst = Dict.Translation.Destination.from_dict(data_dict["dst"])
            return Dict.Translation(data_dict["id"], data_dict["type"], dst)

        def as_dict(self):
            return {
                "id": self.id,
                "type": self.type,
                "dst": self.dst.as_dict()
            }

        def show(self):
            print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))

    def __init__(self, path: str):
        self.path = path
        self.translation_dict: dict[str, Dict.Translation] = {}
        self.load()

    def load(self):
        self.translation_dict.clear()
        with open(self.path, "r", encoding="utf8") as json_file:
            json_dict = json.loads(json_file.read())
            for translation_dict in json_dict["translation_list"]:
                self.translation_dict[translation_dict["id"]] = Dict.Translation.from_dict(translation_dict)

    def save(self):
        pass

    def as_dict(self):
        return {
            "translation_list": [translation.as_dict() for translation in list(self.translation_dict.values())]
        }

    def show(self):
        print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))

class StatDict():

    KEY_LIST = ["id", "err_nb", "total_nb"]

    class Translation():

        def __init__(self, id: str, err_nb: int = 0, total_nb: int = 0):
            self.id = id
            self.err_nb = err_nb
            self.total_nb = total_nb

        @classmethod
        def from_dict(cls, data_dict: dict):
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
        self.entry_dict: dict[str, StatDict.Translation] = {}
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

def main():
    parser = ArgumentParser(description="English vocubulary trainer")
    parser.add_argument("dict_path", type=str, help="Path to dictionnary JSON file")
    parser.add_argument("-s", "--stat", type=str, default="", dest="stat_path", help="Path to statistics CSV file. Default to None")
    parser.add_argument("-n", "--number", type=int, default=QUESTION_NB_DFLT, dest="question_nb",
        help=f"Number of questions to ask. Defaults to {QUESTION_NB_DFLT}")
    args = parser.parse_args()

    translation_dict = Dict(args.dict_path)
    stat_dict = None
    if args.stat_path:
        stat_dict = StatDict(args.stat_path)

    for question_idx in range(args.question_nb):
        print(f"{question_idx + 1} / {args.question_nb}")

        translation_idx = random.randrange(0, len(list(translation_dict.translation_dict.values())))
        translation = list(translation_dict.translation_dict.values())[translation_idx]

        stat = StatDict.Translation(translation.id)
        if stat_dict:
            if translation.id not in stat_dict.entry_dict:
                stat_dict.entry_dict[translation.id] = stat
            else:
                stat = stat_dict.entry_dict[translation.id]

        print(translation.id)
        answer = input()
        if answer == translation.dst.short:
            print("OK")
        else:
            print("ERROR")
            print(translation.dst.short)
            stat.err_nb += 1
        stat.total_nb += 1
        if translation.dst.long:
            print(translation.dst.long)
        if len(translation.dst.example_list) > 0:
            print("Examples :")
            print("\n".join([f"- {ex}" for ex in translation.dst.example_list]))

        print()

    if stat_dict:
        stat_dict.save()

if __name__ == "__main__":
    main()
