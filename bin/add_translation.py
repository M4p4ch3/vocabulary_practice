
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

    add_another = True
    while add_another:
        id = input("- ID : ")
        if id in translation_dict.translation_dict:
            print(f"ERROR Translation ID already in use. Translation : {translation_dict.translation_dict[id].as_str()}")
            print()
            continue

        type = input("- Type (noun, verb, adj): ")

        print("- Destination : ")

        short = input("  - Short : ")
        dst = TranslationDict.Translation.Destination(short)

        long = input("  - Long : ")
        if long:
            dst.long = long

        print("  - Examples (None to exit) : ")
        add_another_ex = True
        while add_another_ex:
            ex_idx = 0
            example = input(f"    - Example {ex_idx + 1} : ")
            if example:
                dst.example_list += [example]
            else:
                add_another_ex = False
            ex_idx += 1

        translation = TranslationDict.Translation(id, type, dst)

        print("Translation :")
        translation.show()
        add = str_to_bool(input("Add ? (y/n) : "))
        if add:
            translation_dict.translation_dict[id] = translation
            translation_dict.save()

        print()
        add_another = str_to_bool(input("Add another ? (y/n) : "))
        print()

if __name__ == "__main__":
    main()
