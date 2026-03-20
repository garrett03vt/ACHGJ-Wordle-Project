"""Utilities for loading and cleaning Wordle word lists."""

from __future__ import annotations
from pathlib import Path
from typing import Iterable, List

DEFAULT_WORD_LENGTH = 5
DEFAULT_WORDS_FILE = Path(__file__).with_name("words.txt")


def clean_words(words: Iterable[str],
                *,
                word_length: int = DEFAULT_WORD_LENGTH,
                normalize_case: bool = True,
                dedupe: bool = True) -> List[str]:
    
    """Clean a list of words by stripping whitespace and optionally converting to lowercase.
            Rules:
            - strip surrounding whitespace
            - optionally lowercase words
            - word mus be purely alphabetic
            - optionally remove duplicates while preserving order
            - keep words of exactly ``word_length``
    """
    cleaned: list[str] = []
    seen: set[str] = set()

    for raw_word in words:
        word = raw_word.strip()
        if normalize_case:
            word = word.lower()

        if len(word) != word_length or not word.isalpha():
            continue

        if dedupe:
            if word in seen:
                continue
            seen.add(word)

        cleaned.append(word)

    return cleaned

def load_word_list(file_path: Path) -> List[str]:
    """Load a list of words from a file."""
    with file_path.open("r", encoding="utf-8") as f:
        return clean_words(f.readlines())
    
def load_words_default() -> List[str]:
    """Load the default list of Wordle words from the project."""
    return load_word_list(DEFAULT_WORDS_FILE)

__all__ = [
    "DEFAULT_WORD_LENGTH",
    "DEFAULT_WORDS_FILE",
    "clean_words",
    "load_word_list",
    "load_words_default",
]