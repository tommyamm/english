#!/usr/bin/python3

import os
import argparse
from auxiliary import *
from autocomplete import enable_autocomplete

PATH = os.path.expanduser("~/projects/python/english/english.md")

def main():
    parser = argparse.ArgumentParser(description="Словарик")
    parser.add_argument("-n", nargs='+', metavar=("ENG", "RUS"),
                        help="добавить новое слово [и контекст]")
    parser.add_argument("-d", metavar="WORD", help="удалить слово")
    parser.add_argument("-s", metavar="PREFIX", help="слова c началом на префикс")
    parser.add_argument("-t", action="store_true", help="тренировка")
    parser.add_argument("-l", action="store_true", help="вывести весь словарь")
    parser.add_argument("-f", action="store_true", help="найти (с autocomplete)")
    parser.add_argument("-o", action="store_true", help="просмотр словаря")
    parser.add_argument("--format", action="store_true", help="переформатировать словарь")
    args = parser.parse_args()

    if not os.path.exists(PATH):
        open(PATH, 'w').close()

    if args.n:
        if len(args.n) < 2:
            print("Добавьте перевод самостоятельно вторым параметром")
            return
        eng = args.n[0]
        rus = args.n[1]
        context = " ".join(args.n[2:]) if len(args.n) > 2 else None
        addWord(PATH, eng, rus, context)
        
    elif args.d:
        deleteWord(PATH, args.d)
    elif args.s:
        showByLetter(PATH, args.s)
    elif args.t:
        train(PATH)
    elif args.l:
        listAll(PATH)
    elif args.o:
        openDict(PATH)
    elif args.format:
        force_format(PATH)
    elif args.f:
        dictionary = makeDict(PATH)
        if not dictionary:
            print("Словарь пуст")
            return
        enable_autocomplete(list(dictionary.keys()))
        query = input("Введите слово: ").strip()
        findWord(PATH, query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()