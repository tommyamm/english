import random
from typing import Dict, Optional, Any
from colorama import Fore, Style
from database.db_rule import VocabularyDB

db = VocabularyDB()

def print_word(word_data: Dict[str, Any], format: bool = True) -> None:
    eng = word_data.get('english')
    rus = word_data.get('otherlg')
    ctx = word_data.get('context')
    
    if not eng or not rus:
        return
    
    max_widths = db.get_max_widths()
    maxEngWidth = max_widths['english']
    maxRusWidth = max_widths['russian']
    
    print(
        f"{Fore.LIGHTCYAN_EX}{eng:^{maxEngWidth}}{Style.RESET_ALL} - " +
        f"{Fore.LIGHTYELLOW_EX}{rus:^{maxRusWidth}}{Style.RESET_ALL}" +
        (f" {Fore.LIGHTMAGENTA_EX}[{ctx}]{Style.RESET_ALL}" if ctx else "")
    )

def add_word(eng: str, rus: str, context: Optional[str] = None) -> None:
    result = db.add_word(english=eng, otherlg=rus, context=context)
    if result.success:
        print(f"Added: {eng}")
    else:
        print(f"Error adding word: {result.message}")

def delete_word(eng: str) -> None:
    result = db.delete_word(english=eng)
    if result.success:
        print(f"Deleted: {eng}")
    else:
        print(f"Error deleting word: {result.message}")

def show_by_letter(letter: str) -> None:
    result = db.search_words(prefix=letter)
    if result.success and result.data:
        for word_data in result.data:
            print_word(word_data)
    else:
        print(f"No words found for letter '{letter}': {result.message}")

def train() -> None:
    result = db.get_all_words()
    if not result.success or not result.data:
        print("The dictionary is empty!")
        return
    
    dictionary_list = result.data
    print("Enter 'exit' or 'quit' to exit")
    while True:
        word_data = random.choice(dictionary_list)
        eng = word_data.get('english')
        rus = word_data.get('otherlg')

        if not eng or not rus:
            continue

        answer = input(f"Translate it: {Fore.LIGHTCYAN_EX}{eng}{Style.RESET_ALL}\n> ").strip()
        if answer in ['exit', 'quit']:
            print("Training session is over!")
            break
        if answer.lower() == rus.lower():
            print(f"{Fore.LIGHTGREEN_EX}✓ Correctly!{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTRED_EX}✗ Incorrectly{Style.RESET_ALL}.", end=" ")
            print(f"Right answer: {Fore.LIGHTYELLOW_EX}{rus}{Style.RESET_ALL}")

def list_all() -> None:
    result = db.get_all_words()
    if not result.success or not result.data:
        print("The dictionary is empty!")
        return
    
    words = result.data  # The data is already sorted by ENGLISH word
    last_letter = None
    for word_data in words:
        eng = word_data.get('english')
        if not eng:
            continue
        current_letter = eng[0].lower()
        if last_letter is None:
            last_letter = current_letter
        if last_letter != current_letter:
            print()
            last_letter = current_letter
        print_word(word_data)

def find_word(query: str) -> None:
    result = db.search_words(prefix=query)
    if result.success and result.data:
        for word_data in result.data:
            print_word(word_data)
    else:
        print(f"No matches found for '{query}': {result.message}")