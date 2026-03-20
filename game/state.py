# game/state.py     Garrette Ritz       3/20/2026
# Tracks game state (guesses, attempts, etc.)

class GameState:
    def __init__(self, secret):
        self.secret = secret
        self.guesses = []

    def add_guess(self, guess, feedback):
        self.guesses.append((guess, feedback))

    def is_solved(self):
        return self.guesses and self.guesses[-1][0] == self.secret