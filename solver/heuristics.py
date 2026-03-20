# solver/heuristics.py     Garrette Ritz       3/20/2026
# Scoring strategies (frequency, entropy, etc.)

import math
from collections import Counter
from game.logic import get_feedback

# limit number of guesses for entropy
MAX_CANDIDATES = 100

# Simple frequency-based scoring. Prefers words with common letters in the remaining possibilities.
def score_word(word, possible_words):
    pattern_counts = Counter()
    
    for secret in possible_words:
        feedback = get_feedback(secret, word)
        pattern_counts[feedback] += 1

    total = len(possible_words)
    entropy = 0.0

    for count in pattern_counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy

# reduce the number of words we evaluate for entropy
def choose_candidate_words(possible_words):
    if len(possible_words) <= MAX_CANDIDATES:
        return possible_words
    
    return sorted(possible_words, key=lambda w: len(set(w)), reverse=True)[:MAX_CANDIDATES]