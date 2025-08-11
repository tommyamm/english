import os
import random
import re
from colorama import Fore, Style
from typing import Dict, Optional, Tuple

russian, context = 0, 1

def printWord(dictionary: Dict[str, Tuple[str, str]], eng: str, format: bool=True) -> None:
    if eng not in dictionary:
        return
    rus = dictionary[eng][russian]
    ctx = dictionary[eng][context]
    lEnglish = lenLongestEgnlish(dictionary) if format is True else len(eng)
    lRussia = lenLongestRussian(dictionary) if format is True else len(rus)

    print(  
        f"{Fore.LIGHTCYAN_EX}{eng:^{lEnglish}}{Style.RESET_ALL} - " +
        f"{Fore.LIGHTYELLOW_EX}{rus:^{lRussia}}{Style.RESET_ALL}" +
        (f" {Fore.LIGHTMAGENTA_EX}[{ctx}]{Style.RESET_ALL}" if ctx else "")
    )

def makeDict(PATH: str) -> Dict[str, Tuple[str, Optional[str]]]:
    result = {}
    if not os.path.exists(PATH):
        return result
    with open(PATH, "r", encoding="utf-8") as file:
        for line in file:
            parsed = unpackLine(line)
            if parsed is None:
                continue
            word, translation, context = parsed
            result[word] = (translation, context)
    return result

def unpackLine(line: str) -> Optional[Tuple[str, str, Optional[str]]]:
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    if '-' not in line:
        return None

    left, right = line.split('-', 1)
    word = left.strip()
    right = right.strip()

    # Ищем контекст в квадратных скобках
    match = re.search(r'\[(.*)\]$', right)
    if match:
        translation = right[:match.start()].strip()
        context = match.group(1).strip()
    else:
        translation = right
        context = None
    return word, translation, context

def lenLongestEgnlish(dictionary: Dict[str, Tuple[str, str]]) -> int:
    return max((len(word) for word in dictionary), default=0)

def lenLongestRussian(dictionary: Dict[str, Tuple[str, str]]) -> int:
    return max((len(word[0]) for word in dictionary.values()), default=0)

def formatFile(PATH: str, dictionary: Dict[str, Tuple[str, Optional[str]]]) -> None:
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
    dictionary = makeDict(PATH)
    formatFile(PATH, dictionary)
    print("Файл отформатирован.")

def addWord(PATH: str, eng: str, rus: str, context: Optional[str] = None) -> None:
    dictionary = makeDict(PATH)

    if eng in dictionary:
        print(f"Слыш, тупой Даун, такое слово уже есть:")
        printWord(dictionary, eng, False)
        return
    
    dictionary[eng] = (rus, context)
    formatFile(PATH, dictionary)

    print("Добавлено:")
    printWord(dictionary, eng, False)

def deleteWord(PATH: str, eng: str) -> None:
    dictionary = makeDict(PATH)

    if eng in dictionary:
        print("Удалено:")
        printWord(dictionary, eng, False)
        del dictionary[eng]
        formatFile(PATH, dictionary)
    else:
        print("Слово не найдено")

def showByLetter(PATH: str, letter: str) -> None:
    dictionary = makeDict(PATH)
    letter = letter.lower()
    words = [w for w in sorted(dictionary, key=lambda w: w.lower()) if w.lower().startswith(letter)]
    if not words:
        print("Нет слов на такую букву")
        return

    for w in words:
        printWord(dictionary, w)

def train(PATH: str) -> None:
    dictionary = makeDict(PATH)
    if not dictionary:
        print("Словарь пуст")
        return
    word = random.choice(list(dictionary.keys()))
    answer = input(f"Переведи: {Fore.LIGHTCYAN_EX}{word}{Style.RESET_ALL}\n> ").strip()
    if answer.lower() == dictionary[word][0].lower():
        print(f"{Fore.LIGHTGREEN_EX}✓ Правильно!{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}✗ Неправильно{Style.RESET_ALL}.", end="")
        print(f"Правильный ответ: {Fore.LIGHTYELLOW_EX}{dictionary[word][0]}{Style.RESET_ALL}")

def listAll(PATH: str) -> None:
    dictionary = makeDict(PATH)
    if not dictionary:
        print("Словарь пуст")
        return
        
    for word in sorted(dictionary, key=lambda w: w.lower()):
        printWord(dictionary, word)

def findWord(PATH: str, query: str) -> None:
    dictionary = makeDict(PATH)
    matches = [w for w in dictionary if w.lower().startswith(query.lower())]
    if not matches:
        print("Совпадений не найдено")
        return
    
    for w in matches:
        printWord(dictionary, w)

def openDict(PATH: str) -> None:
    if not os.path.exists(PATH):
        print("Файл словаря не найден")
        return
    os.system(f"less {PATH}")