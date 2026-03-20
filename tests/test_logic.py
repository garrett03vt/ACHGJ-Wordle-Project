# tests/test_logic.py     Garrette Ritz       3/20/2026
# test the logic/wordle rules

import unittest
from game.logic import get_feedback


class TestLogic(unittest.TestCase):

    # BASIC
    def test_all_green(self):
        self.assertEqual(get_feedback("apple", "apple"), "GGGGG")

    def test_all_gray(self):
        self.assertEqual(get_feedback("apple", "zzzzz"), "BBBBB")

    def test_mixed_feedback(self):
        self.assertEqual(get_feedback("apple", "apron"), "GGBBB")

    def test_all_yellow(self):
        self.assertEqual(get_feedback("abcde", "eabcd"), "YYYYY")

    # DUPLICATE LETTERS
    def test_duplicate_in_secret(self):
        # secret has duplicate 'p'
        self.assertEqual(get_feedback("apple", "apart"), "GGBBB")

    def test_duplicate_in_guess(self):
        # guess has duplicate 'l'
        self.assertEqual(get_feedback("apple", "allee"), "GYBBG")

    def test_duplicate_both(self):
        self.assertEqual(get_feedback("allay", "llama"), "YGYBY")

    def test_overguess_duplicate(self):
        # guess has more of a letter than secret
        self.assertEqual(get_feedback("panel", "apple"), "YYBYY")

    def test_repeated_letter_not_overcounted(self):
        # only one 'a' in secret
        self.assertEqual(get_feedback("crane", "aaaaa"), "BBGBB")

    # EDGE
    def test_no_overlap(self):
        self.assertEqual(get_feedback("stone", "quick"), "BBBBB")

    def test_partial_overlap(self):
        self.assertEqual(get_feedback("stone", "notes"), "YYYYY")

    def test_position_vs_presence(self):
        self.assertEqual(get_feedback("table", "bleat"), "YYYYY")


if __name__ == "__main__":
    unittest.main()