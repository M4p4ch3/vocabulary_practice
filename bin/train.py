
"""
English vocabulary trainer
"""

from argparse import ArgumentParser
import random

from vocab_practice.dict import TranslationDict
from vocab_practice.stat import StatDict

QUESTION_NB_DFLT = 5

def main():
    parser = ArgumentParser(description="English vocubulary trainer")
    parser.add_argument("dict_path", type=str, help="Path to dictionnary JSON file")
    parser.add_argument("-s", "--stat", type=str, default="", dest="stat_path", help="Path to statistics CSV file. Default to None")
    parser.add_argument("-n", "--number", type=int, default=QUESTION_NB_DFLT, dest="question_nb",
        help=f"Number of questions to ask. Defaults to {QUESTION_NB_DFLT}")
    args = parser.parse_args()

    translation_dict = TranslationDict(args.dict_path)
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
