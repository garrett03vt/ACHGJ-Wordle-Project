# game/logic.py     Garrette Ritz       3/20/2026
# wordle rules (evaluate guesses against the target word)

def get_feedback(secret: str, guess: str) -> str:
    feedback = ["B"] * len(secret)
    secret_chars = list(secret)  # Convert to list for mutability

    # first pass: greens
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            feedback[i] = "G"
            secret_chars[i] = None

    # second pass: yellows
    for i in range(len(guess)):
        if feedback[i] == "B" and guess[i] in secret_chars:
            feedback[i] = "Y"
            secret_chars[secret_chars.index(guess[i])] = None

    return ''.join(feedback)