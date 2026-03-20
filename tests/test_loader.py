# test the word loader and cleaning functions
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from data.loader import clean_words, load_word_list, load_words_default

class TestCleanWords(unittest.TestCase):

    def test_clean_words_normalizes_filters_and_dedupes(self):
        raw_words = [
            " Apple\n",
            "BERRY",
            "berry",
            "pear",
            "abc12",
            "toolong",
            "grape",
            " grape ",
        ]

        cleaned = clean_words(raw_words)

        self.assertEqual(cleaned, ["apple", "berry", "grape"])


    def test_clean_words_can_preserve_duplicates_and_case(self):
        raw_words = ["Apple", "Apple", "BERRY"]

        cleaned = clean_words(raw_words, normalize_case=False, dedupe=False)

        self.assertEqual(cleaned, ["Apple", "Apple", "BERRY"])
        
class TestLoadWords(unittest.TestCase):
    def test_load_words_reads_and_cleans_from_file(self):
        tmp_path = Path("temp_test_dir")
        tmp_path.mkdir(exist_ok=True)
        words_file = tmp_path / "words.txt"
        words_file.write_text(" Apple\nabc12\nberry\nberry\npears\nmelon\n", encoding="utf-8")

        loaded = load_word_list(words_file)

        self.assertEqual(loaded, ["apple", "berry", "pears", "melon"])
        words_file.unlink()  # Clean up the temporary file
        tmp_path.rmdir()  # Clean up the temporary directory


    def test_load_words_uses_default_project_word_file(self):
        loaded = load_words_default()

        self.assertTrue(loaded)
        self.assertTrue(all(word.isalpha() for word in loaded))
        self.assertTrue(all(word == word.lower() for word in loaded))
        self.assertTrue(all(len(word) == 5 for word in loaded))
        self.assertEqual(len(loaded), len(set(loaded)))
        
if __name__ == "__main__":
    unittest.main()