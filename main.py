#!/usr/bin/python3 -q
import argparse
from source.auxiliary import *

def main():
    parser = argparse.ArgumentParser(description="Dictionary")
    parser.add_argument("-n", nargs='+', metavar=("ENG", "RUS"),
                        help="add a new word [and context]")
    parser.add_argument("-d", metavar="WORD", help="delete a word")
    parser.add_argument("-l", action="store_true", help="output the entire dictionary")
    parser.add_argument("-s", metavar="PREFIX", help="words with a prefix beginning")
    parser.add_argument("-t", action="store_true", help="training")

    # parser.add_argument("-f", action="store_true", help="find (with autocomplete)")
    args = parser.parse_args()

    if args.n:
        if len(args.n) < 2:
            print("Add the translation yourself with the second parameter!")
            return
        eng = args.n[0]
        rus = args.n[1]
        context = " ".join(args.n[2:]) if len(args.n) > 2 else None
        add_word(eng, rus, context)
        
    elif args.d:
        delete_word(args.d)
    elif args.s:
        show_by_letter(args.s)
    elif args.t:
        train()
    elif args.l:
        list_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()