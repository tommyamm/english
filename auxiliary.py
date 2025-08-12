import os
import re
import random

from typing     import Dict, Optional, Tuple
from colorama   import Fore, Style

russian, context = 0, 1

def print_word(dictionary: Dict[str, Tuple[str, str]], eng: str, format: bool=True) -> None:
    if eng not in dictionary:
        return
    rus = dictionary[eng][russian]
    ctx = dictionary[eng][context]

    maxEngWidth = max_eng_len(dictionary) if format else len(eng)
    maxEngWidth = max_rus_len(dictionary) if format else len(eng)

    print(  
        f"{Fore.LIGHTCYAN_EX}{eng:^{maxEngWidth}}{Style.RESET_ALL} - " +
        f"{Fore.LIGHTYELLOW_EX}{rus:^{maxEngWidth}}{Style.RESET_ALL}" +
        (f" {Fore.LIGHTMAGENTA_EX}[{ctx}]{Style.RESET_ALL}" if ctx else "")
    )

def make_dict(PATH: str) -> Dict[str, Tuple[str, Optional[str]]]:
    result = {}
    if not os.path.exists(PATH):
        return result
    with open(PATH, "r", encoding="utf-8") as file:
        for line in file:
            parsed = unpack_line(line)
            if parsed is None:
                continue
            word, translation, context = parsed
            result[word] = (translation, context)
    return result

def unpack_line(line: str) -> Optional[Tuple[str, str, Optional[str]]]:
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    if '-' not in line:
        return None

    left, right = line.split('-', 1)
    word = left.strip()
    right = right.strip()

    # Looking for the context in square brackets
    match = re.search(r'\[(.*)\]$', right)
    if match:
        translation = right[:match.start()].strip()
        context = match.group(1).strip()
    else:
        translation = right
        context = None
    return word, translation, context

def max_eng_len(dictionary: Dict[str, Tuple[str, str]]) -> int:
    return max((len(word) for word in dictionary), default=0)

def max_rus_len(dictionary: Dict[str, Tuple[str, str]]) -> int:
    return max((len(word[0]) for word in dictionary.values()), default=0)

def format_file(PATH: str, dictionary: Dict[str, Tuple[str, Optional[str]]]) -> None:
    mostLength = max(len(w) for w in dictionary) if dictionary else 0
    sortDict = sorted(dictionary, key=lambda w: w.lower())
    lastLetter = None
    with open(PATH, 'w', encoding='utf-8') as file:
        for word in sortDict:
            letter = word[0].lower()
            if lastLetter is None:
                lastLetter = letter
            if lastLetter != letter:
                file.write('\n')
                lastLetter = letter
            translation, context = dictionary[word]
            if context:
                file.write(f"{word:<{mostLength}} - {translation} [{context}]\n")
            else:
                file.write(f"{word:<{mostLength}} - {translation}\n")

def force_format(PATH: str) -> None:
    dictionary = make_dict(PATH)
    format_file(PATH, dictionary)
    print("The file is formatted.")

def add_word(PATH: str, eng: str, rus: str, context: Optional[str] = None) -> None:
    dictionary = make_dict(PATH)

    if eng in dictionary:
        print(f"Hey, dumb Down, there's already a word like that:")
        print_word(dictionary, eng, False)
        return
    
    dictionary[eng] = (rus, context)
    format_file(PATH, dictionary)

    print("Added:")
    print_word(dictionary, eng, False)

def delete_word(PATH: str, eng: str) -> None:
    dictionary = make_dict(PATH)

    if eng in dictionary:
        print("Deleted:")
        print_word(dictionary, eng, False)
        del dictionary[eng]
        format_file(PATH, dictionary)
    else:
        print("The word was not found!")

def show_by_letter(PATH: str, letter: str) -> None:
    dictionary = make_dict(PATH)
    letter = letter.lower()
    words = [w for w in sorted(dictionary, key=lambda w: w.lower()) if w.lower().startswith(letter)]
    if not words:
        print("There are no words for such a letter!")
        return

    for w in words:
        print_word(dictionary, w)

def train(PATH: str) -> None:
    dictionary = make_dict(PATH)
    if not dictionary:
        print("The dictionary is empty!")
        return
    word = random.choice(list(dictionary.keys()))
    answer = input(f"Translate it: {Fore.LIGHTCYAN_EX}{word}{Style.RESET_ALL}\n> ").strip()
    if answer.lower() == dictionary[word][0].lower():
        print(f"{Fore.LIGHTGREEN_EX}✓ Correctly!{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}✗ Неправильно{Style.RESET_ALL}.", end="")
        print(f"Right answer: {Fore.LIGHTYELLOW_EX}{dictionary[word][0]}{Style.RESET_ALL}")

def list_all(PATH: str) -> None:
    dictionary = make_dict(PATH)
    if not dictionary:
        print("The dictionary is empty!")
        return
    
    last_word = None
    for word in sorted(dictionary, key=lambda w: w.lower()):
        if last_word is None:
            last_word = word
        if last_word[0] != word[0]:
            print()   
            last_word = word 
        print_word(dictionary, word)

def find_word(PATH: str, query: str) -> None:
    dictionary = make_dict(PATH)
    matches = [w for w in dictionary if w.lower().startswith(query.lower())]
    if not matches:
        print("No matches found!")
        return
    
    for w in matches:
        print_word(dictionary, w)

def open_dict(PATH: str) -> None:
    if not os.path.exists(PATH):
        print("The dictionary file was not found!")
        return
    os.system(f"less {PATH}")