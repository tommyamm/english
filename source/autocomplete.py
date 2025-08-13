import readline
from typing import List, Optional

class DictionaryCompleter:
    def __init__(self, words: List[str]):
        self.words = sorted(words, key=str.lower)

    def complete(self, text: str, state: int) -> Optional[str]:
        matches = [w for w in self.words if w.lower().startswith(text.lower())]
        try:
            return matches[state]
        except IndexError:
            return None

def enable_autocomplete(words: List[str]) -> None:
    completer = DictionaryCompleter(words)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")