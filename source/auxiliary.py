import time
import random
from colorama import Fore, Style
from db_rule import VocabularyDB
from typing import Dict, Optional, Any

db = VocabularyDB()


def print_word(word_data: Dict[str, Any], format: bool = True) -> None:
    eng = word_data.get("english")
    rus = word_data.get("otherlg")
    ctx = word_data.get("context")

    if not eng or not rus:
        return

    max_widths = db.get_max_widths()
    maxEngWidth = max_widths["english"]
    maxRusWidth = max_widths["russian"]

    print(
        f"{Fore.LIGHTCYAN_EX}{eng:<{maxEngWidth}}{Style.RESET_ALL} - "
        + f"{Fore.LIGHTYELLOW_EX}{rus:<{maxRusWidth}}{Style.RESET_ALL}"
        + (f" {Fore.LIGHTMAGENTA_EX}[{ctx}]{Style.RESET_ALL}" if ctx else "")
    )


def add_word(eng: str, rus: str, context: Optional[str] = None) -> None:
    result = db.add_word(english=eng, otherlg=rus, context=context)
    if result.success:
        print(f"Added: {eng}")
    else:
        print("Doctor's recommendation: Get checked for dementia.")
        show_by_letter(eng)
        # print(f"Error adding word: {result.message}")


def delete_word(eng: str) -> None:
    result = db.delete_word(english=eng)
    if result.success:
        print(f"Deleted: {eng}")
    else:
        print(f"Error deleting word: {result.message}")


def edit_word(eng: str, new_rus: Optional[str] = None, 
              new_context: Optional[str] = None) -> None:
    result = db.edit_word(english=eng, new_otherlg=new_rus, new_context=new_context)
    if result.success:
        print(f"Updated: {eng}")
    else:
        print(f"Error updating word: {result.message}")


def show_by_letter(letter: str) -> None:
    """Outputs all words starting with the specified letter."""
    result = db.search_words(prefix=letter)

    if not result.success:
        print(f"{Fore.LIGHTRED_EX}Message from db {Style.RESET_ALL}: {result.message}")
        return
    if not result.data:
        print(
            f"{Fore.LIGHTRED_EX}No words found for letter {Style.RESET_ALL} \'{letter}\'"
            )
        return

    for idx, word_data in enumerate(result.data, start=1):
        print(f"{Fore.LIGHTRED_EX}{idx}{Style.RESET_ALL}", end=" ")
        print_word(word_data)


def get_rest(full_string, start_string):
    if full_string.lower().startswith(start_string.lower()):
        return full_string[len(start_string) :]
    return ""


def train() -> None:
    result = db.get_all_words()

    if not result.success or not result.data:
        print("The dictionary is empty!")
        return

    dictionary_list = result.data

    for word in dictionary_list:
        word["last_seen_time"] = 0.0
        word["session_errors"] = 0
        word["session_correct"] = 0

    print("Enter \'exit\' or \'quit\' to exit")
    while True:
        weights = []
        current_time = time.time()

        for word in dictionary_list:
            time_factor = current_time - word["last_seen_time"]
            if word["last_seen_time"] == 0.0:
                time_factor = 1000

            error_factor = word["session_errors"] + 1
            total_weight = time_factor * error_factor
            weights.append(total_weight)

        word_data = random.choices(dictionary_list, weights=weights, k=1)[0]

        eng = word_data.get("english")
        rus = word_data.get("otherlg")
        ctx = word_data.get("context")

        print(f"Translate it: {Fore.LIGHTCYAN_EX}{eng}{Style.RESET_ALL}")
        if ctx:
            print(f"Context: {Fore.LIGHTMAGENTA_EX}{ctx}{Style.RESET_ALL}")
        print("> ", end="")

        answer = input().strip()
        if answer.lower() in ["exit", "quit"]:
            total_answers = 0
            total_correct = 0
            total_incorrect = 0

            for word in dictionary_list:
                total_correct += word["session_correct"]
                total_incorrect += word["session_errors"]

            total_answers = total_correct + total_incorrect

            print("\n" + "=" * 25)
            print(f"{Fore.LIGHTYELLOW_EX}Training Session Summary{Style.RESET_ALL}")
            print("=" * 25)

            if total_answers > 0:
                hardest_words = sorted(
                    [w for w in dictionary_list if w["session_errors"] > 0],
                    key=lambda x: x["session_errors"],
                    reverse=True,
                )

                accuracy = (total_correct / total_answers) * 100

                print(f"Total answers: {total_answers}")
                print(
                    f"  - {Fore.LIGHTGREEN_EX}Correct: {total_correct}{Style.RESET_ALL}"
                )
                print(
                    f"  - {Fore.LIGHTRED_EX}Incorrect: {total_incorrect}{Style.RESET_ALL}"
                )
                print(f"Accuracy: {accuracy:.2f}%")

                if hardest_words:
                    print("\nWords to practice:")
                    for word in hardest_words[:5]:
                        print(
                            f"  - {word['english']} ({Fore.LIGHTRED_EX}{word['session_errors']} errors{Style.RESET_ALL})"
                        )
            else:
                print("You didn't answer any questions.")

            print("=" * 25)
            print("\nTraining session is over!")
            break

        word_data["last_seen_time"] = time.time()

        is_correct = False
        if (
            answer.strip()
            and rus.lower().startswith(answer.lower())
            and answer.lower() != rus.lower()
        ):
            print(
                f"You mean: {answer}{Fore.LIGHTYELLOW_EX}{get_rest(rus, answer)}{Style.RESET_ALL}"
            )
            print(f"{Fore.LIGHTGREEN_EX}✓ Correctly!{Style.RESET_ALL}")
            is_correct = True
        elif answer.lower() == rus.lower():
            print(f"{Fore.LIGHTGREEN_EX}✓ Correctly!{Style.RESET_ALL}")
            is_correct = True
        else:
            print(f"{Fore.LIGHTRED_EX}✗ Incorrectly{Style.RESET_ALL}.", end=" ")
            print(f"Right answer: {Fore.LIGHTYELLOW_EX}{rus}{Style.RESET_ALL}")
            word_data["session_errors"] += 1

        if is_correct:
            word_data["session_correct"] += 1

def list_all() -> None:
    result = db.get_all_words()
    num_of_entries = db.get_num_of_entries()

    if not result.success or not result.data:
        print("The dictionary is empty!")
        return
    
    words = result.data  # The data is already sorted by ENGLISH word

    counter = 0
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
        counter += 1
        print(f"{Fore.LIGHTRED_EX}{counter:<{len(str(num_of_entries)) + 1}}{Style.RESET_ALL}", end="")
        print_word(word_data)
