
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

class TranslationDict():

    class Entry():

        class Language():

            class Entry():

                def __init__(self, short: str, long: str = ""):
                    self.short = short
                    self.long = long

                @classmethod
                def from_dict(cls, data_dict: dict[str, str]):
                    entry = cls(data_dict["short"])
                    if "long" in data_dict:
                        entry.long = data_dict["long"]
                    return entry

                def as_dict(self):
                    data_dict = {
                        "short": self.short
                    }
                    if self.long:
                        data_dict["long"] = self.long
                    return data_dict

            def __init__(self, id: str, entry: Entry):
                self.id = id
                self.entry = entry

            @classmethod
            def from_dict(cls, data_dict: dict[str, Any]):
                entry = TranslationDict.Entry.Language.Entry.from_dict(data_dict["entry"])
                return TranslationDict.Entry.Language(data_dict["id"], entry)

            def as_dict(self):
                return {
                    "id": self.id,
                    "entry": self.entry.as_dict()
                }

        def __init__(self, id: str, type: str):
            self.id = id
            self.type = type
            self.lang_dict: dict[str, TranslationDict.Entry.Language] = {}

        def add_lang(self, lang: Language):
            if lang.id in self.lang_dict:
                return
            self.lang_dict[lang.id] = lang

        def get_lang(self, lang_id: str):
            if lang_id not in self.lang_dict:
                return None
            return self.lang_dict[lang_id]

        @classmethod
        def from_dict(cls, data_dict: dict):
            entry = TranslationDict.Entry(data_dict["id"], data_dict["type"])
            for lang_entry_dict in data_dict["language_list"]:
                entry.add_lang(TranslationDict.Entry.Language.from_dict(lang_entry_dict))
            return entry

        def as_dict(self):
            return {
                "id": self.id,
                "type": self.type,
                "language_list" : [lang_entry.as_dict() for lang_entry in list(self.lang_dict.values())]
            }

        def show(self):
            print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))

    def __init__(self, path: str):
        self.path = path
        self.entry_dict: dict[str, TranslationDict.Entry] = {}
        self.load()

    def load(self):
        self.entry_dict = {}
        with open(self.path, "r", encoding="utf8") as json_file:
            json_dict = json.loads(json_file.read())
            for entry_dict in json_dict["entry_list"]:
                self.entry_dict[entry_dict["id"]] = TranslationDict.Entry.from_dict(entry_dict)

    def save(self):
        pass

    def as_dict(self):
        return {
            "entry_list": [entry.as_dict() for entry in list(self.entry_dict.values())]
        }

    def show(self):
        print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))

class StatDict():

    KEY_LIST = ["id", "err_nb", "total_nb"]

    class Entry():

        def __init__(self, id: str, err_nb: int = 0, total_nb: int = 0):
            self.id = id
            self.err_nb = err_nb
            self.total_nb = total_nb

        @classmethod
        def from_dict(cls, data_dict: dict):
            return StatDict.Entry(
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
        self.entry_dict: dict[str, StatDict.Entry] = {}
        self.load()

    def load(self):
        self.entry_dict = {}
        with open(self.path, "r", encoding="utf8") as csv_file:
            csv_reader = DictReader(csv_file)
            for entry_dict in csv_reader:
                self.entry_dict[entry_dict["id"]] = StatDict.Entry.from_dict(entry_dict)

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
    parser.add_argument("-n", "--number", type=int, default=QUESTION_NB_DFLT,
        help=f"Number of questions to ask. Defaults to {QUESTION_NB_DFLT}")
    args = parser.parse_args()

    translation_dict = TranslationDict("./data/translation.json")
    stat_dict = StatDict("./data/stats.csv")

    for _ in range(args.number):
        translation_idx = random.randrange(0, len(list(translation_dict.entry_dict.values())))
        translation = list(translation_dict.entry_dict.values())[translation_idx]

        if translation.id not in stat_dict.entry_dict:
            stat_dict.entry_dict[translation.id] = StatDict.Entry(translation.id)
        stat = stat_dict.entry_dict[translation.id]

        print(translation.lang_dict["en"].entry.short)
        if translation.lang_dict["en"].entry.long:
            print(translation.lang_dict["en"].entry.long)
        answer = input()
        if answer == translation.lang_dict["fr"].entry.short:
            print("OK")
        else:
            print("ERROR")
            print(translation.lang_dict["fr"].entry.short)
            stat.err_nb += 1
        stat.total_nb += 1
        if translation.lang_dict["fr"].entry.long:
            print(translation.lang_dict["fr"].entry.long)
        print()

    stat_dict.save()

if __name__ == "__main__":
    main()
