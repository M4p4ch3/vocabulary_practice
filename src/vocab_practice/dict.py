
import json
import shutil
from typing import Any, List, Dict

class TranslationDict():

    class Translation():

        class Destination():

            def __init__(self, repr: str):
                self.repr = repr
                self.answer_list: List[str] = []
                self.example_list: List[str] = []

            @classmethod
            def from_dict(cls, data_dict: Dict[str, Any]):
                inst = cls(data_dict["repr"])
                inst.answer_list = [answer for answer in data_dict["answer_list"]]
                if "example_list" in data_dict:
                    inst.example_list = [example for example in data_dict["example_list"]]
                return inst

            def as_dict(self):
                data_dict: Dict[str, Any] = {
                    "repr": self.repr,
                    "answer_list" : [answer for answer in self.answer_list]
                }
                if len(self.example_list) > 0:
                    data_dict["example_list"] = [example for example in self.example_list]
                return data_dict

            def as_str(self):
                return json.dumps(self.as_dict(), indent=4, ensure_ascii=False)

            def show(self):
                print(self.as_str())

        def __init__(self, id: str, type: str, repr: str):
            self.id = id
            self.type = type
            self.repr = repr
            self.dst_list: List[TranslationDict.Translation.Destination] = []

        @classmethod
        def from_dict(cls, data_dict: Dict):
            inst = TranslationDict.Translation(data_dict["id"], data_dict["type"], data_dict["repr"])
            inst.dst_list = [TranslationDict.Translation.Destination.from_dict(dst_dict) for dst_dict in data_dict["dst_list"]]
            return inst

        def as_dict(self):
            return {
                "id": self.id,
                "type": self.type,
                "repr": self.repr,
                "dst_list": [dst.as_dict() for dst in self.dst_list]
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
