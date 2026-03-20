# test_solver.py     Garrette Ritz       3/20/2026
# test the solver/main AI logic

import unittest
import solver.solver as solver


# THIS IS A FAKE get_feedback FUNCTION FOR TESTING PURPOSES ONLY. REPLACE WITH ACTUAL FUNCTION FROM game.logic WHEN READY.
def fake_get_feedback(secret, guess):
    feedback = ["B"] * 5

    # first pass: greens
    for i in range(5):
        if guess [i] == secret[i]:
            feedback[i] = "G"

    # second pass: yellows
    for i in range(5):
        if feedback[i] == "B" and guess[i] in secret:
            feedback[i] = "Y"

    return ''.join(feedback)
solver.get_feedback = fake_get_feedback


# TESTING SOLVER LOGIC
class TestSolver(unittest.TestCase):

    def test_matches_feedback(self):
        word = "apple"
        guess = "apple"
        feedback = "GGGGG"
        self.assertTrue(solver.matches_feedback(word, guess, feedback))


    def test_matches_feedback_false(self):
        word = "angle"
        guess = "apple"
        feedback = "GGGGG"
        self.assertFalse(solver.matches_feedback(word, guess, feedback))


    def test_filter_words(self):
        words = ["apple", "angle", "amble"]
        guess = "apple"
        feedback = fake_get_feedback("angle", guess)  # USED THE FAKE GET SOLVER METHOD. Should be "GGGBB"
        result = solver.filter_words(words, guess, feedback)
        self.assertTrue(all(solver.matches_feedback(w, guess, feedback) for w in result))


    def test_choose_best_guess(self):
        words = ["raise", "alone", "amble"]
        best_guess = solver.choose_best_guess(words)
        self.assertIn(best_guess, words) #should return a valid word from list
    

    def test_filter_reduces_space(self):
        words = ["apple", "angle", "amble", "alien"]
        guess = "apple"
        feedback = fake_get_feedback("angle", guess)  # USED THE FAKE GET SOLVER METHOD. Should be "GGGBB"
        result = solver.filter_words(words, guess, feedback)
        self.assertLessEqual(len(result), len(words))

    def test_solve_word(self):
        secret = "angle"
        words = ["apple", "angle", "amble", "alien"]
        guesses = solver.solve_word(secret, words)
        self.assertEqual(guesses[-1][0], secret)  # Last guess should be the secret word


if __name__ == '__main__':
    unittest.main()