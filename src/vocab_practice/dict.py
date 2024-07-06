
import json
from typing import Any, List, Dict

class TranslationDict():

    class Translation():

        class Destination():

            def __init__(self, short: str, long: str = ""):
                self.short = short
                self.long = long
                self.example_list: List[str] = []

            @classmethod
            def from_dict(cls, data_dict: Dict[str, Any]):
                entry = cls(data_dict["short"])
                if "long" in data_dict:
                    entry.long = data_dict["long"]
                if "example_list" in data_dict:
                    for example in data_dict["example_list"]:
                        entry.example_list += [example]
                return entry

            def as_dict(self):
                data_dict: Dict[str, Any] = {
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
        def from_dict(cls, data_dict: Dict):
            dst = TranslationDict.Translation.Destination.from_dict(data_dict["dst"])
            return TranslationDict.Translation(data_dict["id"], data_dict["type"], dst)

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
        self.translation_dict: Dict[str, TranslationDict.Translation] = {}
        self.load()

    def load(self):
        self.translation_dict.clear()
        with open(self.path, "r", encoding="utf8") as json_file:
            json_dict = json.loads(json_file.read())
            for translation_dict in json_dict["translation_list"]:
                self.translation_dict[translation_dict["id"]] = TranslationDict.Translation.from_dict(translation_dict)

    def save(self):
        pass

    def as_dict(self):
        return {
            "translation_list": [translation.as_dict() for translation in list(self.translation_dict.values())]
        }

    def show(self):
        print(json.dumps(self.as_dict(), indent=4, ensure_ascii=False))
