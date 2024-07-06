
import json
import shutil
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

        def as_str(self):
            return json.dumps(self.as_dict(), indent=4, ensure_ascii=False)

        def show(self):
            print(self.as_str())

    def __init__(self, path: str):
        self.path = path
        self.backup_path = f"{self.path.removesuffix('.json')}_save.json"
        self.translation_dict: Dict[str, TranslationDict.Translation] = {}
        self.load()

    def load(self):
        self.translation_dict.clear()
        with open(self.path, "r", encoding="utf8") as json_file:
            json_dict = json.loads(json_file.read())
            for translation_dict in json_dict["translation_list"]:
                self.translation_dict[translation_dict["id"]] = TranslationDict.Translation.from_dict(translation_dict)

    def _backup(self):
        shutil.copyfile(self.path, self.backup_path)

    def _restore(self):
        shutil.copyfile(self.backup_path, self.path)

    def save(self):
        self._backup()
        try:
            with open(self.path, "w", encoding="utf8") as json_file:
                json_file.write(self.as_str())
        except Exception:
            print("ERROR save to file FAILED. Restoring")
            self._restore()

    def as_dict(self):
        return {
            "translation_list": [translation.as_dict() for translation in list(self.translation_dict.values())]
        }

    def as_str(self):
        return json.dumps(self.as_dict(), indent=4, ensure_ascii=False)

    def show(self):
        print(self.as_str())
