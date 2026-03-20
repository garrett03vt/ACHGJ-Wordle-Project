# heuristics.py     Garrette Ritz       3/20/2026
# Scoring strategies (frequency, entropy, etc.)

from collections import Counter

# Simple frequency-based scoring. Prefers words with common letters in the remaining possibilities.
def score_word(word, possible_words):
    letter_counts = Counter()
    
    for w in possible_words:
        for letter in set(w):
            letter_counts[letter] += 1

    score = 0
    for letter in set(word):
        score += letter_counts[letter]

    return score