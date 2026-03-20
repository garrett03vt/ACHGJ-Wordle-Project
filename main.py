# main.py     Garrette Ritz       3/20/2026
# main file for project, runs the game and connects everything

import random
from data.loader import load_words_default
from solver.solver import solve_word

# Convert GYB to emojis for better visualization
def format_feedback(feedback):
    mapping = {"G": "🟩", "Y": "🟨", "B": "⬛"}
    return "".join(mapping[c] for c in feedback)

def run_single_game(words):
    secret = random.choice(words)

    print("ACHGJ WORDLE SOLVER")
    print("-------------------")
    print(f"(debug) Secret word: {secret}\n")  # DEBUGGING PURPOSES ONLY - REMOVE IN PRODUCTION

    guesses = solve_word(secret, words)

    print("\nGuesses and Feedback:")
    for i, (guess,feedback) in enumerate(guesses, 1):
        emoji = format_feedback(feedback)
        print(f"{i}: {guess.upper()} {emoji}")

    print(f"\n✅ Solved in {len(guesses)} guesses!\n")

def run_simulation(words, n=50):
    total_guesses = 0
    print(f"Running simulation ({n} games)...")
    for i in range(n):
        secret = random.choice(words)
        guesses = solve_word(secret, words)
        total_guesses += len(guesses)

    avg = total_guesses / n
    print(f"Average guesses over {n} games: {avg:.2f}")

def main():
    words = load_words_default()

    run_single_game(words)

    run_simulation(words, n=50)

if __name__ == "__main__":
    main()