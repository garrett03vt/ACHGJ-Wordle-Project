# solver/heuristics.py     Garrette Ritz       3/20/2026
# Scoring strategies (frequency, entropy, etc.)

import math
from collections import Counter
from game.logic import get_feedback

# limit number of guesses for entropy
MAX_CANDIDATES = 100


def score_word(word, possible_words):
    """
    Compute the Shannon entropy of the feedback patterns for a given guess.

    :param word: The guess word to evaluate.
    :param possible_words: The list of remaining possible secret words.
    :return: A floating point score representing the entropy. Higher is better.
    """
    pattern_counts: Counter[str] = Counter()
    # Build a distribution of feedback patterns given this guess
    for secret in possible_words:
        feedback = get_feedback(secret, word)
        pattern_counts[feedback] += 1

    total = len(possible_words)
    entropy = 0.0
    # Compute Shannon entropy over the distribution of patterns
    for count in pattern_counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


# -----------------------------------------------------------------------------
# Frequency‑based heuristics

def _build_letter_frequency(possible_words: list[str]) -> Counter:
    """
    Build a frequency table counting how many of the remaining possible words
    contain each letter. Each word contributes at most one count per letter,
    regardless of how many times that letter appears in the word. This helps
    prioritise letters that are common across many words.

    :param possible_words: The list of remaining possible secret words.
    :return: A collections.Counter mapping letters to counts.
    """
    freq: Counter[str] = Counter()
    for w in possible_words:
        for c in set(w):  # count each letter once per word
            freq[c] += 1
    return freq


def score_word_frequency(word: str, possible_words: list[str]) -> int:
    """
    Score a guess word based solely on letter frequencies in the remaining
    candidate words. The score is the sum of frequencies of the unique letters
    in ``word``. A higher score indicates that the word covers more common
    letters and is therefore likely to glean useful information about the secret.

    :param word: The guess word to evaluate.
    :param possible_words: The list of remaining possible secret words.
    :return: An integer score; larger is better.
    """
    freq = _build_letter_frequency(possible_words)
    # Sum the frequencies for each unique letter in the word
    return sum(freq[c] for c in set(word))


def choose_best_guess_frequency(possible_words: list[str]) -> str:
    """
    Pick the next guess using the simple frequency heuristic. We optionally
    reduce the candidate set using the same ``choose_candidate_words`` utility
    used by the entropy heuristic. Among these candidates we compute the
    frequency‑based score and return the word with the highest score.

    :param possible_words: The list of remaining possible secret words.
    :return: The selected guess word.
    """
    candidates = choose_candidate_words(possible_words)
    freq = _build_letter_frequency(possible_words)
    best_score = -1
    best_word: str | None = None
    for word in candidates:
        score = sum(freq[c] for c in set(word))
        if score > best_score:
            best_score = score
            best_word = word
    # Fallback: if best_word is None (e.g. empty list), just return first candidate
    return best_word if best_word is not None else (candidates[0] if candidates else "")

# reduce the number of words we evaluate for entropy
def choose_candidate_words(possible_words):
    if len(possible_words) <= MAX_CANDIDATES:
        return possible_words
    
    return sorted(possible_words, key=lambda w: len(set(w)), reverse=True)[:MAX_CANDIDATES]