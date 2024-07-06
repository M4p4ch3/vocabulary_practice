
"""
Add transaltion to dictionnary
"""

from argparse import ArgumentParser

from vocab_practice.dict import TranslationDict

QUESTION_NB_DFLT = 5

def str_to_bool(data_str: str):
    if "n" in data_str.lower():
        return False
    return True

def main():
    parser = ArgumentParser(description="Add translation to dictionnary")
    parser.add_argument("dict_path", type=str, help="Path to dictionnary JSON file")
    args = parser.parse_args()

    translation_dict = TranslationDict(args.dict_path)

    print("Translations :")
    translation_idx = 0
    while True:
        print(f"- Translation {translation_idx + 1} :")

        id = input("  - ID : ")
        if not id:
            break

        if id in translation_dict.translation_dict:
            print(f"ERROR Translation ID already in use. Translation : {translation_dict.translation_dict[id].as_str()}")
            print()
            continue

        type = input("  - Type (noun, verb, adj): ")
        repr = input("  - Representation : ")

        translation = TranslationDict.Translation(id, type, repr)

        print("  - Destinations :")
        dst_idx = 0
        while True:
            print(f"    - Destination {dst_idx + 1} :")

            repr = input("      - Representation : ")
            if not repr:
                break

            dst = TranslationDict.Translation.Destination(repr)

            print("      - Answers :")
            answer_idx = 0
            while True:
                answer = input(f"        - Answer {answer_idx + 1} : ")
                if not answer:
                    break
                dst.answer_list += [answer]
                answer_idx += 1

            print("      - Examples : ")
            ex_idx = 0
            while True:
                example = input(f"        - Example {ex_idx + 1} : ")
                if not example:
                    break
                dst.example_list += [example]
                ex_idx += 1

            print(f"    - Destination {dst_idx + 1} :")
            dst.show()
            add = str_to_bool(input("  Add ? (y/n) : "))
            if add:
                translation.dst_list += [dst]

            dst_idx += 1
            print()

        print(f"  Translation {translation_idx} :")
        translation.show()
        add = str_to_bool(input("Add ? (y/n) : "))
        if add:
            translation_dict.translation_dict[id] = translation
            translation_dict.save()

        translation_idx += 1
        print()

if __name__ == "__main__":
    main()
