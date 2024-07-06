
"""
English vocabulary trainer
"""

from argparse import ArgumentParser
import random
import unicodedata

from vocab_practice.dict import TranslationDict
from vocab_practice.stat import StatDict

QUESTION_NB_DFLT = 5

def to_ascii(data: str):
    return unicodedata.normalize("NFKD", data).encode("ASCII","ignore").decode("ascii")

def main():
    parser = ArgumentParser(description="English vocubulary trainer")
    parser.add_argument("dict_path", type=str, help="Path to dictionnary JSON file")
    parser.add_argument("-s", "--stat", type=str, default="", dest="stat_path", help="Path to statistics CSV file. Default to None")
    parser.add_argument("-n", "--number", type=int, default=QUESTION_NB_DFLT, dest="question_nb",
        help=f"Number of questions to ask. Defaults to {QUESTION_NB_DFLT}")
    args = parser.parse_args()

    translation_dict = TranslationDict(args.dict_path)
    translation_dict.show()
    stat_dict = None
    if args.stat_path:
        stat_dict = StatDict(args.stat_path)

    for question_idx in range(args.question_nb):
        print(f"{question_idx + 1} / {args.question_nb}")

        translation_idx = random.randrange(0, len(list(translation_dict.translation_dict.values())))
        translation = list(translation_dict.translation_dict.values())[translation_idx]
        print(translation.repr)

        stat = StatDict.Translation(translation.id)
        if stat_dict:
            if translation.id not in stat_dict.entry_dict:
                stat_dict.entry_dict[translation.id] = stat
            else:
                stat = stat_dict.entry_dict[translation.id]

        answer_ok_list = []
        for dst in translation.dst_list:
            answer_ok_list += [to_ascii(answer.lower()) for answer in dst.answer_list]
        print(answer_ok_list)

        if to_ascii(input().lower()) in answer_ok_list:
            print("OK")
        else:
            print("ERROR")
            stat.err_nb += 1

        print("Destinations : [")
        for dst in translation.dst_list:
            dst.show()
        print("]")

        stat.total_nb += 1
        print()

    if stat_dict:
        stat_dict.save()

if __name__ == "__main__":
    main()
