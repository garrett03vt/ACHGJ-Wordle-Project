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
            - optionally remove duplicates while preserving order
            - keep words of exactly ``word_length``
    """
    cleaned = []
    seen = set() if dedupe else None
    
    for word in words:
        word = word.strip()
        if normalize_case:
            word = word.lower()
        if len(word) == word_length:
            if not dedupe or (seen is not None and word not in seen):
                cleaned.append(word)
                if seen is not None:
                    seen.add(word)
    
    return cleaned

def load_word_list(file_path: Path) -> List[str]:
    """Load a list of words from a file."""
    with file_path.open("r", encoding="utf-8") as f:
        return clean_words(f.readlines())

__all__ = [
    "DEFAULT_WORD_LENGTH",
    "DEFAULT_WORDS_FILE",
    "clean_words",
    "load_word_list",
]