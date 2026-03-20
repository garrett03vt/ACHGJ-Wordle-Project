# solver/solver.py     Garrette Ritz       3/20/2026
# main solving loop and picks next best guess

from solver.heuristics import score_word
from game.logic import get_feedback         

# Check if a word matches the feedback for a given guess
def matches_feedback(word, guess, feedback):
    return get_feedback(word, guess) == feedback


# Remove words that don't match the feedback
def filter_words(words, guess, feedback):
    return [w for w in words if matches_feedback(w, guess, feedback)]


# Pick the highest scoring word
def choose_best_guess(possible_words):
    best_score = -1
    best_word = None

    for word in possible_words:
        score = score_word(word, possible_words)
        if score > best_score:
            best_score = score
            best_word = word

    return best_word


# Wordle solver. Returns a list of (guess, feedback)
def solve_word(secret, all_words):
    possible_words = all_words.copy()
    guesses = []

    while True:
        guess = choose_best_guess(possible_words)
        feedback = get_feedback(secret, guess)

        guesses.append((guess, feedback))

        # FOR DEBUGGING PURPOSES ONLY - PRINT EACH GUESS AND FEEDBACK
        # print(f"Guess {len(guesses)}: {guess} -> {feedback} | Remaining: {len(possible_words)}")
        # FOR DEBUGGING PURPOSES ONLY - PRINT EACH GUESS AND FEEDBACK
        
        if guess == secret:
            break
        possible_words = filter_words(possible_words, guess, feedback)

        if not possible_words:
            raise ValueError("No possible words left! Something went wrong.")
    
    return guesses

