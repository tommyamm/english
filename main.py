#!/usr/bin/python3

import os
import argparse
from auxiliary import *
from autocomplete import enable_autocomplete

PATH = os.path.expanduser("~/projects/python/english/english.md")

def main():
    parser = argparse.ArgumentParser(description="Dictionary")
    parser.add_argument("-n", nargs='+', metavar=("ENG", "RUS"),
                        help="add a new word [and context]")
    parser.add_argument("-d", metavar="WORD", help="delete a word")
    parser.add_argument("-s", metavar="PREFIX", help="words with a prefix beginning")
    parser.add_argument("-t", action="store_true", help="training")
    parser.add_argument("-l", action="store_true", help="output the entire dictionary")
    parser.add_argument("-f", action="store_true", help="find (with autocomplete)")
    parser.add_argument("-o", action="store_true", help="viewing the dictionary")
    parser.add_argument("--format", action="store_true", help="reformat the dictionary")
    args = parser.parse_args()

    if not os.path.exists(PATH):
        open(PATH, 'w').close()

    if args.n:
        if len(args.n) < 2:
            print("Add the translation yourself with the second parameter!")
            return
        eng = args.n[0]
        rus = args.n[1]
        context = " ".join(args.n[2:]) if len(args.n) > 2 else None
        add_word(PATH, eng, rus, context)
        
    elif args.d:
        delete_word(PATH, args.d)
    elif args.s:
        show_by_letter(PATH, args.s)
    elif args.t:
        train(PATH)
    elif args.l:
        list_all(PATH)
    elif args.o:
        open_dict(PATH)
    elif args.format:
        force_format(PATH)
    elif args.f:
        dictionary = make_dict(PATH)
        if not dictionary:
            print("The dictionary is empty!")
            return
        enable_autocomplete(list(dictionary.keys()))
        query = input("Enter the word: ").strip()
        find_word(PATH, query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()