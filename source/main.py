#!/usr/bin/python3 -q
import sys
from auxiliary import *

# PS: unfortunately, argparse did not fit

USAGE = """\
Usage: eng [-n ENG RUS [CONTEXT]] [-d WORD] [-l] [-s PREFIX] [-t]

English Vocabulary Helper

Options:
  -h,                      show this help message and exit
  -n ENG RUS [CONTEXT]     add a new word [and context]
  -d WORD                  delete a word
  -e WORD TRLATE [CONTEXT] edit entry: word, new translation, [new context]
  -l                       output the entire dictionary
  -s PREFIX                words with a prefix beginning
  -t                       training\
"""
def print_usage():
    print(USAGE)

def main():
    args = sys.argv[1:]  # Skip the script name

    if args in [None, "-h"]:
        print_usage()
        return

    if "-n" in args:
        idx = args.index("-n")
        if idx + 2 >= len(args):
            print("Add the translation yourself with the second parameter!")
            return
        eng = args[idx + 1]
        rus = args[idx + 2]
        context = " ".join(args[idx + 3:]) if idx + 3 < len(args) else None
        add_word(eng, rus, context)

    elif "-d" in args:
        idx = args.index("-d")
        if idx + 1 >= len(args):
            print("Please provide a word to delete!")
            return
        delete_word(args[idx + 1])

    elif "-e" in args:
        idx = args.index("-e")
        if idx + 1 >= len(args):
            print("Please provide a word to edit!")
            return
        eng = args[idx + 1]
        new_rus = args[idx + 2] if idx + 2 < len(args) else None
        new_context = " ".join(args[idx + 3:]) if idx + 3 < len(args) else None
        edit_word(eng, new_rus, new_context)

    elif "-s" in args:
        idx = args.index("-s")
        if idx + 1 >= len(args):
            print("Please provide a prefix!")
            return
        show_by_letter(args[idx + 1])

    elif "-t" in args:
        train()

    elif "-l" in args:
        list_all()

    else:
        print_usage()

if __name__ == "__main__":
    main()